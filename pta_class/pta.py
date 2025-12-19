import json
import time
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from requests import Session, Response
from loguru import logger

from pta_class.ExamProblemTypes.examProblemTypes import (
    ExamProblemTypesLabel,
    ExamProblemTypesLabelId,
)
from .browser_login import login as web_login
from .Exam import Exam
from .ExamProblemTypes import ExamProblemTypes
from .Problems.problems import Problems, ProblemsId
from .Submission.submission import (
    Submission,
    SubmissionId,
)


def get_time_str() -> str:
    """获取当前时间（UTC 时间）并格式化为 ISO 8601 格式的时间戳"""
    current_time = datetime.now(timezone.utc)
    formatted_time = current_time.isoformat()
    return formatted_time


login_url = "https://passport.pintia.cn/api/users/sessions"
problem_set_url = "https://pintia.cn/api/problem-sets"
problem_submission_url = (
    "https://pintia.cn/api/exams/{exam_id}/problem-sets/{problems_id}/user-submissions"
)
exam_url = "https://pintia.cn/api/problem-sets/{problems_id}/exams"
problem_list_url = "https://pintia.cn/api/problem-sets/{problems_id}/exam-problem-types"
submission_url = "https://pintia.cn/api/submissions/{submission_id}"
exam_problems_url = (
    "https://pintia.cn/api/problem-sets/{problems_id}/exam-problems/{problem_id}"
)
headers = {
    "Sec-Ch-Ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "Accept-Language": "zh-CN",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json;charset=UTF-8",
    "Origin": "https://pintia.cn",
    "Referer": "https://pintia.cn/",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
}


class pta:
    RETRY_STATUS = {429}

    def __init__(
        self,
        email: str = "",
        password: str = "",
        retries: int = 3,
        backoff: float = 0.5,
    ):
        self.email = email
        self.password = password
        self.cookies: dict[str, str] = {}
        self.session = Session()
        self.retries = int(retries)
        self.backoff = float(backoff)
        self.user_id: str = ""
        self.problem_sets: list[Problems] = []
        self.exam_info: dict[ProblemsId, Exam] = {}
        self.problems_list: dict[ProblemsId, ExamProblemTypes] = {}
        self.submission_list: dict[
            ExamProblemTypesLabelId, dict[SubmissionId, Submission]
        ] = {}

    def __enter__(self) -> "pta":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """关闭底层 Session"""
        self.session.close()

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
        retries: int = 3,
        backoff: float = 0.5,
        cookies: Optional[dict[str, str]] = None,
    ) -> Response:
        """统一的请求入口，处理重试与默认头/凭据。"""

        last_response: Optional[Response] = None
        for attempt in range(retries + 1):
            logger.trace(
                f"HTTP {method} {url} attempt={attempt+1}/{retries+1} params={params} payload={(payload and '...') or None}"
            )
            response = self.session.request(
                method,
                url,
                params=params,
                json=payload,
                cookies=cookies or self.cookies,
                headers=headers,
            )
            last_response = response

            if response.status_code in self.RETRY_STATUS and attempt < retries:
                delay = backoff * (2**attempt)
                logger.warning(
                    f"Rate limited ({response.status_code}). Backing off {delay:.2f}s then retrying..."
                )
                time.sleep(delay)
                continue

            logger.debug(
                f"HTTP {method} {url} status={response.status_code} len={len(response.content) if response.content is not None else 0}"
            )
            return response

        # 如果走到这里，说明重试后仍失败，返回最后一次响应供上层处理
        assert last_response is not None
        return last_response

    @staticmethod
    def _parse_json(response: Response) -> Optional[dict[str, Any]]:
        try:
            return response.json()
        except Exception:
            return None

    def _request_json(
        self,
        method: str,
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
        retries: Optional[int] = None,
        backoff: Optional[float] = None,
        on_error: Optional[Callable[[Response], None]] = None,
    ) -> tuple[bool, Optional[dict[str, Any]]]:
        response = self._request(
            method,
            url,
            params=params,
            payload=payload,
            retries=self.retries if retries is None else retries,
            backoff=self.backoff if backoff is None else backoff,
        )
        data = self._parse_json(response)

        if response.ok:
            logger.trace(
                f"JSON OK {method} {url} keys={list(data.keys()) if isinstance(data, dict) else 'N/A'}"
            )
            return True, data

        if on_error:
            on_error(response)
        logger.error(
            f"JSON ERR {method} {url} status={response.status_code} body={(data if isinstance(data, dict) else response.text[:200])}"
        )
        return False, data

    def _api_get(
        self, url: str, *, params: Optional[dict[str, Any]] = None
    ) -> tuple[bool, Optional[dict[str, Any]]]:
        return self._request_json("GET", url, params=params)

    def _api_post(
        self, url: str, *, payload: Optional[dict[str, Any]] = None
    ) -> tuple[bool, Optional[dict[str, Any]]]:
        return self._request_json("POST", url, payload=payload)

    @staticmethod
    def _print_error(action: str, data: Optional[dict[str, Any]]) -> None:
        code = (
            (data or {}).get("error", {}).get("code")
            if isinstance(data, dict)
            else None
        )
        logger.error(f"{action}失败: {data}\n错误码: {code}")

    @property
    def is_logged_in(self) -> bool:
        return bool(self.cookies)

    def logout(self) -> None:
        logger.info("Logging out and clearing cookies")
        self.cookies = {}
        self.session.cookies.clear()

    def login(self, nocookies: bool = False) -> bool:
        """登录函数"""
        if (not nocookies) and self.read_cookies():
            return True

        payload = {
            "email": self.email,
            "password": self.password,
            "rememberMe": False,
        }
        response = self._request("POST", login_url, payload=payload)
        data = self._parse_json(response) or {}

        if response.status_code == 200:
            self.cookies = self.session.cookies.get_dict()
            logger.info("登录成功（API）")
            return True

        if response.status_code == 415:
            logger.error("登录失败")
            return False

        if response.status_code == 400:
            message = data.get("error", {}).get("message", "登录失败")
            logger.error(message)
            if data.get("error", {}).get("code") == "GATEWAY_WRONG_CAPTCHA":
                logger.warning("存在图形验证码，是否打开浏览器登录？(y/n)")
                choice = input().lower()
                if choice == "y":
                    return self.browser_login()
            return False

        logger.error(f"未知的错误:{data or response.text}")
        return False

    def browser_login(self) -> bool:
        """使用浏览器登录"""
        try:
            cookies = web_login(self.email, self.password)
        except Exception as e:
            logger.exception(f"发生错误: {e}")
            return False
        self.cookies.update({str(i["name"]): str(i["value"]) for i in cookies})
        self.session.cookies.update(self.cookies)
        logger.info("登录成功（浏览器）")
        return True

    def get_problems(self) -> bool:
        payload = {"filter": {"endAtAfter": get_time_str()}}
        success, data = self._request_json("GET", problem_set_url, payload=payload)
        if success and data:
            self.problem_sets += [Problems(i) for i in data.get("problemSets", [])]
            logger.info(f"已获取题目集数量: {len(self.problem_sets)}")
            return True

        if data and data.get("error", {}).get("code") == "USER_NOT_FOUND":
            choice = input("是否重新登录？(y/n)")
            if choice.lower() == "y":
                self.cookies = {}
                self.session.cookies.clear()
                self.login(nocookies=True)
                return self.get_problems()
            raise Exception("用户不存在")

        if data:
            self._print_error("获取题库", data)
        return False

    def get_exam(self, problems: Problems) -> bool:
        if problems.id in self.exam_info.keys():
            logger.debug(f"考试信息已缓存: {problems.id}")
            return True
        url = exam_url.format(problems_id=problems.id)
        success, data = self._api_get(url)
        if success and data:
            self.exam_info[problems.id] = Exam(data["exam"])
            logger.info(f"获取考试信息成功: {problems.id}")
            return True
        if data:
            self._print_error("获取考试信息", data)
        return False

    def get_problem_list(self, problems: Problems) -> bool:
        if problems.id in self.problems_list.keys():
            logger.debug(f"题目列表已缓存: {problems.id}")
            return True
        url = problem_list_url.format(problems_id=problems.id)
        success, data = self._api_get(url)
        if success and data:
            self.problems_list[problems.id] = ExamProblemTypes(data)
            logger.info(
                f"获取题目列表成功: {problems.id}, 题目数={len(self.problems_list[problems.id].labels)}"
            )
            return True
        if data:
            self._print_error("获取题目信息", data)
        return False

    def get_submission_list(
        self,
        problems: Problems,
        exam: Exam,
        problemid: ExamProblemTypesLabelId,
    ) -> bool:
        url = problem_submission_url.format(exam_id=exam.id, problems_id=problems.id)
        payload = {"limit": 50, "filter": str({"problemSetProblemId": problemid})}
        success, data = self._api_get(url, params=payload)
        if success and data:
            if problemid not in self.submission_list.keys():
                self.submission_list[problemid] = {}
            for i in data.get("submissions", []):
                submission = Submission(i)
                self.submission_list[problemid][submission.id] = submission
            logger.debug(
                f"获取提交列表成功: problemId={problemid}, 提交数={len(self.submission_list[problemid])}"
            )
            return True

        if data:
            self._print_error("获取提交信息", data)
        return False

    def get_submission_info(self, submission: Submission):
        url = submission_url.format(submission_id=submission.id)
        success, data = self._api_get(url)
        if success and data:
            new_data = Submission(data["submission"])
            submission.update(new_data)
            logger.debug(
                f"获取提交详情成功: submissionId={submission.id}, status={submission.status}, score={submission.score}"
            )
            return True

        if data:
            self._print_error("获取提交详情", data)
        return False

    def get_problem_description(
        self, problemsid: ProblemsId, problem: ExamProblemTypesLabel
    ) -> bool:
        url = exam_problems_url.format(problems_id=problemsid, problem_id=problem.id)
        success, data = self._api_get(url)
        if success and data:
            problem.update(ExamProblemTypesLabel(data["problemSetProblem"]))
            logger.debug(
                f"获取题目描述成功: problemsId={problemsid}, labelId={problem.id}"
            )
            return True
        if data:
            self._print_error("获取题目描述", data)
        return False

    def save_cookies(self, path: str = "data.json") -> bool:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.cookies,
                f,
                ensure_ascii=False,
                indent=4,
            )
        logger.info(f"Cookies 已保存到 {path}")
        return True

    def read_cookies(self, path: str = "data.json") -> bool:
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.cookies = json.load(f)
            self.session.cookies.update(self.cookies)
            logger.info(f"Cookies 已从 {path} 读取")
            return True
        except FileNotFoundError:
            logger.warning("Cookie文件不存在")
            return False
        except json.JSONDecodeError:
            logger.error("Cookie文件格式错误")
            return False
        except Exception as e:
            logger.exception(f"发生错误: {e}")
            return False
