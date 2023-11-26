from dataclasses import asdict, dataclass


@dataclass
class BaseEntity:
    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __post_init__(self) -> None:
        self.validation()

    def validation(self) -> None:
        raise NotImplementedError(f"{self.__class__} not implement validation method!")

    def to_dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}
