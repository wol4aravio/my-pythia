from abc import ABC, abstractmethod


class AbstractProcessor(ABC):
    @abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, _, __, ___):
        raise NotImplementedError()

    @abstractmethod
    def send(self, message: str, topic: str, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def subscribe(self, topic, *args, **kwargs):
        raise NotImplementedError()
