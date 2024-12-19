from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.llms._ollama import OllamaLLMModule
from utils.generators import FluxHuggingFaceGenerator
from base import GenerativeQuery
import dotenv

dotenv.load_dotenv()


def main():
    mod = OllamaLLMModule.from_env()
    flux = FluxHuggingFaceGenerator.from_env()

    query = GenerativeQuery("an Iphone 15", 4)

    response = mod.generate(query)

    print(response.descriptions)

    img = flux.generate(response.descriptions[0], inference_steps=20, guidance_scale=3.5)

    img.show()


if __name__ == "__main__":
    main()
