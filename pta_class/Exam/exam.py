from ..Base import BaseData, BaseScore, BaseId

class ExamId(BaseId):
    """exam的id"""
    pass

class ExamScore(BaseScore):
    """exam的分数"""
    pass

class Exam(BaseData):
    """exam的基本信息"""
    id: ExamId
    score: ExamScore
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

