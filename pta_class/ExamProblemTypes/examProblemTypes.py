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


class ExamProblemTypesLabelContent(str):
    """题目的内容"""


class ExamProblemTypesLabelDescription(str):
    """题目的描述"""


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
    content: ExamProblemTypesLabelContent = ExamProblemTypesLabelContent()
    description: ExamProblemTypesLabelDescription = ExamProblemTypesLabelDescription()

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
        super().__init__(*args, **kwargs)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "labels":
            super().__setattr__(key, [ExamProblemTypesLabel(item) for item in value])
        elif key == "examLabelByProblemSetProblemId":
            super().__setattr__(
                key,
                {
                    ExamProblemTypesLabelId(k): ExamProblemTypesLabelNumber(v)
                    for k, v in value.items()
                },
            )
        else:
            return super().__setattr__(key, value)
