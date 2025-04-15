import json
from requests import Session
from datetime import datetime, timezone

from pta_class.ExamProblemTypes.examProblemTypes import ExamProblemTypesLabel, ExamProblemTypesLabelId
from .browser_login import login as web_login

from .Problems.problems import Problems, ProblemsId
from .Exam import Exam
from .ExamProblemTypes import ExamProblemTypes
from .Submission.submission import (
    Submission,
    SubmissionId,
    SubmissionProblemSetProblemId,
)

from datetime import datetime, timezone


def time() -> str:
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
    def __init__(self, email: str="", password: str=""):
        self.email = email
        self.password = password
        self.cookies: dict[str, str] = {}
        self.user_id: str = ""
        self.problem_sets: list[Problems] = []
        self.exam_info: dict[ProblemsId, Exam] = {}
        self.problems_list: dict[ProblemsId, ExamProblemTypes] = {}
        self.submission_list: dict[ExamProblemTypesLabelId, dict[SubmissionId, Submission]] = {}

    def login(self) -> bool:
        """登录函数"""
        if self.read_cookies():
            return True
        payload = {
            "email": self.email,
            "password": self.password,
            "rememberMe": False,
        }
        with Session() as session:
            response = session.post(login_url, json=payload, headers=headers)
            if response.status_code == 200:
                self.cookies = session.cookies.get_dict()
                return True
            else:
                if response.status_code == 415:
                    print("登录失败")
                    return False
                elif response.status_code == 400:
                    print(f'{response.json()["error"]["message"]}')
                    if response.json()["error"]["code"] == "GATEWAY_WRONG_CAPTCHA":
                        print("存在图形验证码，是否打开浏览器登录？(y/n)")
                        choice = input().lower()
                        if choice == "y":
                            return self.browser_login()
                        return False
                    return False
                else:
                    print(f"未知的错误:{response.json()}")
                    return False

    def browser_login(self) -> bool:
        """使用浏览器登录"""
        try:
            cookies = web_login(self.email,self.password)
        except Exception as e:
            print(f"发生错误: {e}")
            return False
        self.cookies.update({str(i["name"]): str(i["value"]) for i in cookies})
        return True

    def get_problems(self) -> bool:
        payload = {"filter": {"endAtAfter": time()}}
        with Session() as session:
            requsets = session.get(problem_set_url, json=payload, cookies=self.cookies,headers=headers)
            if requsets.status_code == 200:
                problem_set = requsets.json()
                self.problem_sets += [Problems(i) for i in problem_set["problemSets"]]
                return True
            else:
                print(
                    f"获取题库失败: {requsets.json()}\n错误码: {requsets.status_code}"
                )
                return False

    def get_exam(self, problems: Problems) -> bool:
        if problems.id in self.exam_info.keys():
            return True
        url = exam_url.format(problems_id=problems.id)
        with Session() as session:
            requests = session.get(url, cookies=self.cookies,headers=headers)
            if requests.status_code == 200:
                exam_info = requests.json()
                self.exam_info[problems.id] = Exam(exam_info["exams"])
                return True
            else:
                print(
                    f"获取考试信息失败: {requests.json()}\n错误码: {requests.status_code}"
                )
                return False

    def get_problem_list(self, problems: Problems) -> bool:
        if problems.id in self.problems_list.keys():
            return True
        url = problem_list_url.format(problems_id=problems.id)
        with Session() as session:
            requests = session.get(url, cookies=self.cookies,headers=headers)
            if requests.status_code == 200:
                problem_list_info = requests.json()
                self.problems_list[problems.id] = ExamProblemTypes(
                    problem_list_info["examProblemTypes"]
                )
                return True
            else:
                print(
                    f"获取题目信息失败: {requests.json()}\n错误码: {requests.status_code}"
                )
                return False

    def get_submission_list(
        self,
        problems: Problems,
        exam: Exam,
        problemid: ExamProblemTypesLabelId,
    ) -> bool:
        url = problem_submission_url.format(exam_id=exam.id, problems_id=problems.id,headers=headers)
        payload = {
            "filter": {
                "problemSetProblemId": problemid,
            }
        }
        with Session() as session:
            requests = session.get(url, json=payload, cookies=self.cookies)
            if requests.status_code == 200:
                submission_list = requests.json()
                for i in submission_list["submissions"]:
                    submission = Submission(i)
                    self.submission_list[problemid][submission.id] = submission
                return True
            else:
                print(
                    f"获取提交信息失败: {requests.json()}\n错误码: {requests.status_code}"
                )
                return False

    def get_submission_info(self, submission: Submission):
        url = submission_url.format(submission_id=submission.id)
        with Session() as session:
            requests = session.get(url, cookies=self.cookies,headers=headers)
            if requests.status_code == 200:
                submission_info = requests.json()
                new_data = Submission(submission_info["submission"])
                submission.updata(new_data)
                return True
            else:
                print(
                    f"获取提交信息失败: {requests.json()}\n错误码: {requests.status_code}"
                )
                return False

    def save_cookies(self, path: str='data.json') -> bool:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.cookies, f, ensure_ascii=False, indent=4, )
        return True

    def read_cookies(self, path: str='data.json') -> bool:
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.cookies = json.load(f)
            return True
        except FileNotFoundError:
            print("Cookie文件不存在")
            return False
        except json.JSONDecodeError:
            print("Cookie文件格式错误")
            return False
        except Exception as e:
            print(f"发生错误: {e}")
            return False