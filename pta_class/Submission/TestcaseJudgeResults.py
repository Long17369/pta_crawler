from ..Base import *


class Result(str):
    """测试结果"""


class Exceed(str):
    """超出限制类型"""


class Time(float):
    """运行时间"""


class Memory(int):
    """内存使用"""


class Exitcode(int):
    """退出码"""


class Termsig(int):
    """终止信号"""


class Error(str):
    """错误信息"""


class Stdout(str):
    """标准输出"""


class Stderr(str):
    """标准错误输出"""


class CheckerOutput(str):
    """检查器输出"""


class TestcaseScore(BaseScore):
    """测试用例分数"""


class StdoutTruncated(BaseBool):
    """标准输出是否截断"""


class StderrTruncated(BaseBool):
    """标准错误输出是否截断"""


class ShowOutput(BaseBool):
    """是否显示输出"""


class TestcaseJudgeResults(BaseData):
    """测试用例评测结果"""

    result: Result = Result()
    exceed: Exceed = Exceed()
    time: Time = Time()
    memory: Memory = Memory()
    exitcode: Exitcode = Exitcode()
    termsig: Termsig = Termsig()
    error: Error = Error()
    stdout: Stdout = Stdout()
    stderr: Stderr = Stderr()
    checkerOutput: CheckerOutput = CheckerOutput()
    testcaseScore: TestcaseScore = TestcaseScore()
    stdoutTruncated: StdoutTruncated = StdoutTruncated()
    stderrTruncated: StderrTruncated = StderrTruncated()
    showOutput: ShowOutput = ShowOutput()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
