from requests import get, post
from datetime import datetime, timedelta, timezone

from pta_class import *

email: str
password: str


def time() -> str:

    # 获取当前时间（UTC 时间）
    current_time = datetime.now(timezone.utc)

    # 如果需要在当前时间基础上加一段时间（例如加1天）
    # 可以使用 timedelta
    # future_time = current_time + timedelta(days=1)

    # 格式化为 ISO 8601 格式的时间戳
    formatted_time = current_time.isoformat()

    return formatted_time


class pta:

    pta_login_url = "https://passport.pintia.cn/api/users/sessions"
    pta_problem_set_url = "https://pintia.cn/api/problem-sets"
    pta_problem_submission_url = "https://pintia.cn/api/exams/{exam_id}/problem-sets/{problems_id}/user-submissions"
    pta_problem_exam_url = "https://pintia.cn/api/problem-sets/{problems_id}/exams"
    pta_problem_list_url = (
        "https://pintia.cn/api/problem-sets/{problems_id}/exam-problem-types"
    )
    submission_url = "https://pintia.cn/api/submissions/{submission_id}"

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.session = None
        self.exam_info: dict[ProblemsId, Exam] = dict()
        self.problems_list: dict[ProblemsId, ExamProblemTypes] = dict()
        self.problem_sets: list[Problems] = list()
        self.submission_list: dict[ProblemsId, dict[SubmissionId, Submission]] = dict()

    def login(self) -> bool:
        post_data = {
            "email": self.email,
            "password": self.password,
            "rememberMe": False,
        }
        headers = {"Content-Type": "content-type:application/json;charset=UTF-8"}
        login_post = post(
            self.pta_login_url,
            data=post_data,
            headers=headers
        )
        login_info = dict(login_post.json())
        if login_info.get("error", None) == None:
            self.session = login_post.cookies.get_dict()
            print("登录成功")
            return True
        elif login_info["error"]["code"] == "GATEWAY_WRONG_CAPTCHA":
            print(login_info["error"]["message"])
            print("存在图形验证码，请手动获取id及cookies")
            return False
        elif (
            login_info["error"]["code"] == "USER_SERVICE_INCORRECT_USERNAME_OR_PASSWORD"
        ):
            print(login_info["error"]["code"])
            return False
        else:
            print(f"未知的错误:{login_info['error']}")
        return False

    def get_problem_sets(self) -> bool:
        get_problem_sets_data = {"filter": {"endAtAfter": time()}}
        problem_set_get = get(
            self.pta_problem_set_url, data=get_problem_sets_data, cookies=self.session
        )
        if problem_set_get.ok:
            problem_set_info = problem_set_get.json()
            problem_sets = problem_set_info["problemSets"]
            for i in problem_sets:
                self.problem_sets.append(Problems(i))
            return True
        else:
            return False

    def get_submission_list(
        self,
        problems_id: ProblemsId,
        exam: Exam,
        problem_set_problem_id: SubmissionProblemSetProblemId,
    ) -> bool:
        # if self.problem[]
        url = self.pta_problem_submission_url.format(
            exam_id=exam.id, problems_id=problems_id
        )
        submission_data = {
            "filter": {
                "problemSetProblemId": problem_set_problem_id,
            }
        }
        submission_get = get(url, data=submission_data, cookies=self.session)
        submission_info = submission_get.json()
        if submission_get.ok:
            submission_list = submission_info["submissions"]
            for i in submission_list:
                submission = Submission(i)
                self.submission_list[problems_id][submission.id] = submission
            return True
        else:
            return False

    def get_problem_list(self, problems_id: ProblemsId):
        if problems_id in self.problems_list:
            return True
        url = self.pta_problem_list_url.format(problem_id=problems_id)
        problem_list_get = get(url, cookies=self.session)
        problem_list_info = problem_list_get.json()
        if problem_list_get.ok:
            self.problems_list[problems_id] = ExamProblemTypes(
                problem_list_info["examProblemTypes"]
            )
            return True
        else:
            return False
        pass

    def get_exam_info(self, problems_id: ProblemsId):
        if problems_id in self.exam_info:
            return True
        url = self.pta_problem_exam_url.format(problems_id=problems_id)
        exam_get = get(url, cookies=self.session)
        exam_info = exam_get.json()
        if exam_get.ok:
            self.exam_info[problems_id] = Exam(exam_info["exams"])
            return True
        else:
            return False

    def get_submission_info(self, submission: Submission): ...
