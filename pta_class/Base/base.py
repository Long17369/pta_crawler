class BaseScore(float):
    """分数基类"""


class BaseId(str):
    """id基类"""


class BaseBool:
    """布尔值基类"""

    data: bool

    def __init__(self, data: 'bool|BaseBool' = False) -> None:
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
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        self.other[key] = value
            elif isinstance(args[0], BaseData):
                for key, value in args[0].__dict__.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        self.other[key] = value
            else:
                raise TypeError(f"Cannot convert {type(args[0])} to {self.__class__}")
        else:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    self.other[key] = value
        pass

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found")

    def __iter__(self):
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
            if hasattr(self, key):
                super().__setattr__(key, type(getattr(self,key))(value))
            else:
                super().__setattr__(key, value)
        elif key == 'other':
            super().__setattr__(key,value)
        else:
            self.other[key] = value

    def to_dict(self) -> dict:
        res = dict()
        for k,v in self:
            if isinstance(v,BaseData):
                res[k] = v.to_dict()
            elif isinstance(v,list):
                res[k] = [i.to_dict() if isinstance(i,BaseData) else i for i in v]
            elif isinstance(v,dict):
                res[k] = {k2:v2.to_dict() if isinstance(v2,BaseData) else v2 for k2,v2 in v.items()}
            elif isinstance(v,BaseBool):
                res[k] = bool(v)
            else:
                res[k] = v
        return res
