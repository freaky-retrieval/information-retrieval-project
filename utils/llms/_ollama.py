import os
import tenacity
from typing import Optional
from base._dtos import GenerativeQuery, GenerativeQueryResponse
from utils.llms._base import BaseLLMPipelineModule, BaseLLMPipelineModuleConfig
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.exceptions import OutputParserException


class OllamaLLMPipelineModuleConfig(BaseLLMPipelineModuleConfig):
    def __init__(
        self,
        model: str,
        temperature: float,
        maximum_length_per_caption: int,
        maximum_tokens: int = 2048,
        retry_attempts: int = 5,
    ):
        super().__init__(
            model, maximum_length_per_caption, maximum_tokens, retry_attempts
        )
        self.temperature = temperature

    @classmethod
    def from_env(cls):
        return cls(
            model=os.getenv("LLM_MODEL"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0.8)),
            maximum_length_per_caption=int(os.getenv("LLM_MAX_LENGTH", 77)),
            maximum_tokens=int(os.getenv("LLM_MAX_TOKENS", 2048)),
            retry_attempts=int(os.getenv("LLM_MAX_RETRIES", 5)),
        )


class OllamaLLMPipelineModule(BaseLLMPipelineModule):
    def __init__(self, config: OllamaLLMPipelineModuleConfig):
        super().__init__(config)

        self.llm = ChatOllama(
            model=self.config.model,
            temperature=self.config.temperature,
            num_predict=self.config.maximum_tokens,
        )

        self.prompt_template = PromptTemplate(
            input_variables=["prompt", "samples", "max_tokens"],
            template="""
            You are an expert in refining user's prompt with {samples} enhanced descriptions for a diffusion model to generate a SKETCH image.

            The caption must emphasize a black-and-white sketch with no color. The length of each description should be {max_tokens} tokens.

            You are given a prompt:

            {prompt}

            Format the output as a JSON object with the following key-value pair: "descriptions": ["description1", "description2", "description3", ...]
            """,
        )

        self.chain = self.prompt_template | self.llm | SimpleJsonOutputParser()

    def generate(self, prompt: GenerativeQuery) -> Optional[GenerativeQueryResponse]:
        def _vunerable_call():
            response = self.chain.invoke(
                {
                    "prompt": prompt.query,
                    "samples": prompt.samples,
                    "max_tokens": self.config.max_length_per_caption,
                }
            )

            return GenerativeQueryResponse(samples=response["descriptions"])

        try:
            return tenacity.retry(
                _vunerable_call,
                wait=tenacity.wait_fixed(0.25),
                stop=tenacity.stop_after_attempt(self.config.retry_attempts),
                reraise=True,
            )()
        except OutputParserException:
            return None

    @classmethod
    def from_env(cls):
        return cls(config=OllamaLLMPipelineModuleConfig.from_env())
