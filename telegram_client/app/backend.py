from abc import ABC, abstractmethod

class BaseBackend(ABC):

    @abstractmethod
    def call(self, query):
        raise NotImplementedError

class Backend(BaseBackend):

    def __init__(self) -> None:
        pass

    def call(self, query: str) -> str:
        return f"your response - {query}"

