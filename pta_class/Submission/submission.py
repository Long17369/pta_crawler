from typing import Any
from ..Base import *
from ..Problems.problems import ProblemsId
from .JudgeResponseContents import JudgeResponseContents


class SubmissionId(str):
    """提交的id"""


class SubmissionUserId(str):
    """提交的用户id"""


class SubmissionProblemType(str):
    """提交的题目类型"""


class SubmissionProblemSetProblemId(str):
    """提交的题目集问题id"""


class SubmissionSubmitAt(str):
    """提交的时间"""


class SubmissionStatus(str):
    """提交的状态"""


class SubmissionScore(BaseScore):
    """提交的分数"""


class SubmissionCompiler(str):
    """提交使用的编译器"""


class SubmissionTime(float):
    """提交的运行时间"""


class SubmissionMemory(int):
    """提交的内存使用"""


class SubmissionPreviewSubmission(BaseBool):
    """是否为预览提交"""


class SubmissionJudgeAt(str):
    """判题时间"""


class SubmissionCause(str):
    """判题原因"""


class ProgrammingSubmissionDetail(BaseData):
    """提交的编程详情"""

    class Compiler(str):
        """提交使用的编译器"""

    class Program(str):
        """提交的代码"""

    compiler: Compiler = Compiler()
    program: Program = Program()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class ProblemId(str):
    """提交的题目id (不知道是啥玩意)"""


class SubmissionDetails(BaseData):

    problemSetProblemId: SubmissionProblemSetProblemId = SubmissionProblemSetProblemId()
    programmingSubmissionDetail: ProgrammingSubmissionDetail = (
        ProgrammingSubmissionDetail()
    )
    codeCompletionSubmissionDetail: ProgrammingSubmissionDetail = (
        ProgrammingSubmissionDetail()
    )
    problemId: ProblemId = ProblemId()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Submission(BaseData):

    id: SubmissionId = SubmissionId()
    userId: SubmissionUserId = SubmissionUserId()
    problemType: SubmissionProblemType = SubmissionProblemType()
    problemSetProblemId: SubmissionProblemSetProblemId = SubmissionProblemSetProblemId()
    submitAt: SubmissionSubmitAt = SubmissionSubmitAt()
    status: SubmissionStatus = SubmissionStatus()
    score: SubmissionScore = SubmissionScore()
    compiler: SubmissionCompiler = SubmissionCompiler()
    time: SubmissionTime = SubmissionTime()
    memory: SubmissionMemory = SubmissionMemory()
    previewSubmission: SubmissionPreviewSubmission = SubmissionPreviewSubmission()
    judgeAt: SubmissionJudgeAt = SubmissionJudgeAt()
    cause: SubmissionCause = SubmissionCause()
    problemSetId: ProblemsId = ProblemsId()
    submissionDetails: list[SubmissionDetails]
    judgeResponseContents: list[JudgeResponseContents]

    def __init__(self, *args, **kwargs) -> None:
        super().__setattr__("submissionDetails", [])
        super().__setattr__("judgeResponseContents", [])
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "submissionDetails":
            for i in value:
                self.submissionDetails.append(SubmissionDetails(i))
        elif name == "judgeResponseContents":
            for i in value:
                self.judgeResponseContents.append(JudgeResponseContents(i))
        else:
            super().__setattr__(name, value)

    def update(self, other: "Submission") -> None:
        """更新提交信息"""
        for k, v in other:
            if k in self.__dict__:
                setattr(self, k, v)
            else:
                self.other[k] = v
