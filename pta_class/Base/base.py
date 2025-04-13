class BaseScore(float):
    """分数基类"""


class BaseId(str):
    """id基类"""


class BaseBool:
    """布尔值基类"""

    data: bool

    def __init__(self, data: bool = False) -> None:
        self.data = data

    def __bool__(self) -> bool:
        return self.data


class BaseData:
    """数据基类"""

    def __init__(self, *args, **kwargs) -> None:
        self.other = dict()
        if len(args) == 1:
            if isinstance(args[0], dict):
                for key, value in args[0].items():
                    if isinstance(value, list|dict):
                        continue
                    if hasattr(self, key):
                        setattr(self, key, type(getattr(self, key))(value))
                    else:
                        self.other[key] = value
            elif isinstance(args[0], list):
                for key, value in zip(self.__annotations__.keys(), args[0]):
                    if isinstance(value, list|dict):
                        continue
                    if hasattr(self, key):
                        setattr(self, key, type(getattr(self, key))(value))
                    else:
                        self.other[key] = value
        else:
            for key, value in kwargs.items():
                if isinstance(value, list|dict):
                    continue
                if hasattr(self, key):
                    setattr(self, key, type(getattr(self, key))(value))
                else:
                    self.other[key] = value
        pass

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found")

    def union(self, other: "BaseData") -> None:
        if type(self) != type(other):
            raise TypeError(f"Cannot union {type(self)} and {type(other)}")
        for key in self.__annotations__.keys():
            if key == "other":
                self.other.update(other.other)
            if hasattr(other, key):
                setattr(self, key, getattr(other, key))

    def __iter__(self):
        for key in self.__annotations__.keys():
            if key == "other":
                for k, v in getattr(self, key):
                    yield k, v
                continue
            yield key, getattr(self, key)
