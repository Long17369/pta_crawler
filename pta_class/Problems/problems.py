from ..Base import *


class ProblemsId(BaseId):
    """题目集的id"""


class ProblemsName(str):
    """题目集的名字"""


class ProblemsType(str):
    """题目集的类型"""


class ProblemsTimeType(str):
    """题目集的时间类型"""


class ProblemsStatus(str):
    """题目集的状态"""


class ProblemsOrganizationName(str):
    """题目集的组织名称"""


class ProblemsOwnerNickname(str):
    """题目集的拥有者昵称"""


class ProblemsManageable(BaseBool):
    """题目集是否可管理"""


class Problems(BaseData):
    """题目集"""

    id: ProblemsId = ProblemsId()
    name: ProblemsName = ProblemsName()
    type: ProblemsType = ProblemsType()
    timeType: ProblemsTimeType = ProblemsTimeType()
    status: ProblemsStatus = ProblemsStatus()
    organizationName: ProblemsOrganizationName = ProblemsOrganizationName()
    ownerNickname: ProblemsOwnerNickname = ProblemsOwnerNickname()
    manageable: ProblemsManageable = ProblemsManageable()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
