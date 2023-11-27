from dataclasses import asdict, dataclass, field


@dataclass
class BaseEntity:
    _id: str | None = field(init=False, default=None)

    @property
    def id(self) -> str | None:
        return self._id

    def set_id(self, id: str):
        self._id = id

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __post_init__(self) -> None:
        self.validation()

    def validation(self) -> None:
        raise NotImplementedError(f"{self.__class__} not implement validation method!")

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}
