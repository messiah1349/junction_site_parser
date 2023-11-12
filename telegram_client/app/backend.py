from abc import ABC, abstractmethod
from rag.call_llm import get_llm_response

class BaseBackend(ABC):

    @abstractmethod
    def call(self, query):
        raise NotImplementedError

class Backend(BaseBackend):

    def __init__(self) -> None:
        pass

    def call(self, query: str) -> str:
        response = get_llm_response(query)
        return response

