from typing import Any
from ..Base import *
from ..Problems.problems import ProblemsId
from .TestcaseJudgeResults import TestcaseJudgeResults


class JudgeResponseContentsStatus(str):
    """判题状态"""


class JudgeResponseContentsScore(BaseScore):
    """判题分数"""


class CompilationResultLog(str):
    """编译日志"""


class CompilationResultSuccess(BaseBool):
    """编译是否成功"""


class CompilationResultError(str):
    """编译错误信息"""


class CheckerCompilationResultLog(str):
    """编译日志"""


class CheckerCompilationResultSuccess(BaseBool):
    """编译是否成功"""


class CheckerCompilationResultError(str):
    """编译错误信息"""


class CompilationResult(BaseData):
    """编译结果"""

    log: CompilationResultLog = CompilationResultLog()
    success: CompilationResultSuccess = CompilationResultSuccess()
    error: CompilationResultError = CompilationResultError()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class CheckerCompilationResult(BaseData):
    """编译结果
    checker 是啥玩意？为啥会有俩?
    """

    log: CheckerCompilationResultLog = CheckerCompilationResultLog()
    success: CheckerCompilationResultSuccess = CheckerCompilationResultSuccess()
    error: CheckerCompilationResultError = CheckerCompilationResultError()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class ProgrammingJudgeResponseContent(BaseData):
    """编程题判题结果
    这个类的设计是为了兼容不同的编程题判题系统(???)"""

    compilationResult: CompilationResult = CompilationResult()
    checkerCompilationResult: CheckerCompilationResult = CheckerCompilationResult()
    testcaseJudgeResults: dict[str, TestcaseJudgeResults] = {}
    problemSetProblemId: ProblemsId = ProblemsId()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'testcaseJudgeResults':
            for k,v in value:
                self.testcaseJudgeResults[k] = TestcaseJudgeResults(v)
        else:
            super().__setattr__(name, value)


class JudgeResponseContents(BaseData):
    status: JudgeResponseContentsStatus = JudgeResponseContentsStatus()
    score: JudgeResponseContentsScore = JudgeResponseContentsScore()
    programmingJudgeResponseContent: ProgrammingJudgeResponseContent = (
        ProgrammingJudgeResponseContent()
    )
    problemSetProblemId: ProblemsId = ProblemsId()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
