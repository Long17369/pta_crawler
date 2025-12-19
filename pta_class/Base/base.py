from typing import Any, get_origin, get_args, Iterator


class BaseScore(float):
    """分数基类"""


class BaseId(str):
    """id基类"""


class BaseBool:
    """布尔值基类"""

    data: bool

    def __init__(self, data: "bool|BaseBool" = False) -> None:
        self.data = bool(data)

    def __bool__(self) -> bool:
        return self.data

    def __repr__(self) -> str:
        return str(self.data)

    def __str__(self) -> str:
        return str(self.data)


class BaseData:
    """数据基类"""

    def __init__(self, *args, **kwargs) -> None:
        self.other = dict()
        if len(args) == 1:
            if isinstance(args[0], dict):
                for key, value in args[0].items():
                    if key in self.__annotations__:
                        setattr(self, key, value)
                    else:
                        self.other[key] = value
            elif isinstance(args[0], BaseData):
                for key, value in args[0].__dict__.items():
                    if key in self.__annotations__:
                        setattr(self, key, value)
                    else:
                        self.other[key] = value
            else:
                raise TypeError(f"Cannot convert {type(args[0])} to {self.__class__}")
        else:
            for key, value in kwargs.items():
                if key in self.__annotations__:
                    setattr(self, key, value)
                else:
                    self.other[key] = value
        pass

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found")

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        for key in self.__dict__.keys():
            if key == "other":
                for k, v in self.other.items():
                    yield k, v
                continue
            yield key, getattr(self, key)

    def __repr__(self) -> str:
        data = dict(self)
        return f"{self.__class__.__name__}({data})"

    def __str__(self) -> str:
        data = dict(self)
        return f"{data}"

    def __setattr__(self, key, value) -> None:
        if key in self.__annotations__.keys():
            ann = self.__annotations__[key]
            converted = self._convert_to_annotation(ann, value)
            super().__setattr__(key, converted)
        elif key == "other":
            super().__setattr__(key, value)
        else:
            self.other[key] = value

    @staticmethod
    def _convert_to_annotation(ann: Any, value: Any) -> Any:
        """根据注解类型将 value 转换为对应类型（递归处理 List/Dict/BaseData）。"""
        origin = get_origin(ann)
        args = get_args(ann)

        # 处理 List[T]
        if origin is list and args:
            elem_type = args[0]
            return [
                BaseData._convert_to_annotation(elem_type, v) for v in (value or [])
            ]

        # 处理 Dict[K, V]
        if origin is dict and len(args) == 2:
            key_t, val_t = args
            converted = {}
            for k, v in (value or {}).items():
                new_k = BaseData._convert_scalar(key_t, k)
                new_v = BaseData._convert_to_annotation(val_t, v)
                converted[new_k] = new_v
            return converted

        # 处理 BaseData 子类
        try:
            if isinstance(value, ann):
                return value
        except Exception:
            ...

        try:
            if isinstance(value, BaseData) and isinstance(value, ann):
                return value
        except Exception:
            ...

        if isinstance(value, dict) and BaseData._is_base_data_subclass(ann):
            return ann(value)

        # 标量类型与包装类型（str/int/float/自定义子类）
        return BaseData._convert_scalar(ann, value)

    @staticmethod
    def _convert_scalar(typ: Any, value: Any) -> Any:
        """将 value 转换为 typ 对应的标量或简单包装类型。"""
        try:
            if BaseData._is_base_data_subclass(typ):
                return typ(value)  # BaseBool/BaseId/BaseScore 等
            # 对于 str/int/float 或其子类
            return typ(value)
        except Exception:
            return value

    @staticmethod
    def _is_base_data_subclass(typ: Any) -> bool:
        try:
            return issubclass(typ, (BaseData, BaseBool, BaseId, BaseScore))
        except Exception:
            return False

    def to_dict(self) -> dict:
        res = dict()
        for k, v in self:
            if isinstance(v, BaseData):
                res[k] = v.to_dict()
            elif isinstance(v, list):
                res[k] = [i.to_dict() if isinstance(i, BaseData) else i for i in v]
            elif isinstance(v, dict):
                res[k] = {
                    k2: v2.to_dict() if isinstance(v2, BaseData) else v2
                    for k2, v2 in v.items()
                }
            elif isinstance(v, BaseBool):
                res[k] = bool(v)
            else:
                res[k] = v
        return res

    def update(self, other: "BaseData|dict") -> None:
        """用另一个 BaseData 或字典更新当前对象（仅更新已声明字段）。"""
        src: dict[str, Any]
        if isinstance(other, BaseData):
            src = dict(other)
        elif isinstance(other, dict):
            src = other
        else:
            raise TypeError("update expects BaseData or dict")

        for key, value in src.items():
            if key in self.__annotations__:
                setattr(self, key, value)
            else:
                self.other[key] = value
