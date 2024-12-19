import os
from base._core import BasePipelineModule
from base._dtos import GenerativeQuery, GenerativeQueryResponse


class LLMModuleConfig:
    def __init__(
        self,
        model: str,
        max_length_per_caption: int = 256,
        maximum_tokens: int = 2048,
        retry_attempts: int = 3,
    ):
        self.model = model
        self.max_length_per_caption = max_length_per_caption
        self.maximum_tokens = maximum_tokens
        self.retry_attempts = retry_attempts

    @classmethod
    def from_env(cls):
        return cls(
            model=os.getenv("LLM_MODEL"),
            num_predicts=int(os.getenv("LLM_NUM_PREDICTS", 256)),
            maximum_tokens=int(os.getenv("LLM_MAX_TOKENS", 2048)),
            retry_attempts=int(os.getenv("LLM_MAX_RETRIES", 5)),
        )


class LLMModule(BasePipelineModule):
    def __init__(self, config: LLMModuleConfig):
        super().__init__()
        self.config = config

    def generate(self, prompt: GenerativeQuery) -> GenerativeQueryResponse:
        raise NotImplementedError
