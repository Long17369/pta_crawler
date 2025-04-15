from typing import Any
from ..Base import *


class ExamProblemTypesLabelId(str):
    """题目的id"""


class ExamProblemTypesLabelNumber(str):
    """题目的题号"""


class ExamProblemTypesLabelScore(BaseScore):
    """题目的分数"""


class ExamProblemTypesLabelProblemPoolCompositionCount(int):
    """题目在题库中的索引 (好像不对)"""


class ExamProblemTypesLabelTitle(str):
    """题目的标题"""


class ExamProblemTypesLabelType(str):
    """题目的类型 (不知道对不对)"""


class ExamProblemTypesLabelIndex(int):
    """题目在题目集内的索引"""


class ExamProblemTypesLabelLabel(str):
    """题目的标签 (没见过，全是空的)"""


class ExamProblemTypesLabelIndexInProblemPool(int):
    """题目在题库中的索引 (好像不对)"""


class ExamProblemTypesLabel(BaseData):
    """题目的各种属性"""

    id: ExamProblemTypesLabelId = ExamProblemTypesLabelId()
    lable: ExamProblemTypesLabelLabel = ExamProblemTypesLabelLabel()
    score: ExamProblemTypesLabelScore = ExamProblemTypesLabelScore()
    problemPoolIndex: ExamProblemTypesLabelIndex = ExamProblemTypesLabelIndex()
    problemPoolCompositionCount: ExamProblemTypesLabelProblemPoolCompositionCount = (
        ExamProblemTypesLabelProblemPoolCompositionCount()
    )
    title: ExamProblemTypesLabelTitle = ExamProblemTypesLabelTitle()
    type: ExamProblemTypesLabelType = ExamProblemTypesLabelType()
    indexInProblemPool: ExamProblemTypesLabelIndexInProblemPool = (
        ExamProblemTypesLabelIndexInProblemPool()
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class ExamProblemTypesProblemTypes:
    """未知类，目前不知道有什么属性"""


class ExamProblemTypes(BaseData):
    labels: list[ExamProblemTypesLabel]
    problemTypes: list[ExamProblemTypesProblemTypes]
    examLabelByProblemSetProblemId: dict[
        ExamProblemTypesLabelId, ExamProblemTypesLabelNumber
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__setattr__('labels',[])
        super().__setattr__('problemTypes',[])
        super().__setattr__('examLabelByProblemSetProblemId',{})
        super().__init__(*args, **kwargs)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "labels":
            for item in value:
                self.labels.append(ExamProblemTypesLabel(item))
        elif key == "examLabelByProblemSetProblemId":
            for key, item in value.items():
                self.examLabelByProblemSetProblemId[ExamProblemTypesLabelId(key)] = (
                    ExamProblemTypesLabelNumber(item)
                )
        else:
            return super().__setattr__(key, value)
