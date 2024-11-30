import re

import aiohttp

from utils.logger import log

class TextModel():
    def __init__(self) -> None:
        op: str = "src.ollama.TextModel.__init__"

        log.debug(f"Initializing ml model interface class [{op}]")

        self.url = "http://localhost:11434/api/generate"

        self.headers = {
            "Content-Type": "application/json"
        }

        # Pre-configured prompt template
        self.default_prompt = """
        You are an AI assistant trained to summarize texts and generate useful metadata. Given the input text, perform the following tasks:

        1. **Summarize the Text**: Provide a concise summary of the key points in the text, ensuring that the summary does not exceed 100 words, while retaining the most important information.
        2. **Generate Metadata**: Extract and generate the following metadata based on the text:
           - **Keywords**: A list of 5 to 10 keywords or phrases that best represent the text.

        Respond using JSON.

        ### Input Text:
        """

    async def summary(self, text: str) -> str | None:
        op: str = "src.ollama.TextModel.query"

        prompt = self.default_prompt + "\n" + text

        payload = {
            "model": "phi3",
            "prompt": prompt,
            "format": "json",
            "stream": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload, headers=self.headers) as response:
                    if response.status == 200:
                        result: dict = await response.json()
                        text: str = result.get("response", "no response field found")

                        # Remove newline characters
                        text = text.replace("\n", " ")

                        # Replace multiple spaces with a single space and strip leading/trailing spaces
                        text = re.sub(r'\s+', ' ', text).strip()

                        # Remove quotes and curly braces
                        text = re.sub(r'[{}"]', '', text)

                        return text
                    else:
                        log.error(f"API request failed with status {response.status} [{op}]")
                        return None

        except Exception as e:
            log.error(f"Error during API request [{op}] \n{e}")
            raise


class Embeddings():
    def __init__(self) -> None:
        op: str = "src.ollama.Embeddings.__init__"

        log.debug(f"Initializing text embeddings interface class [{op}]")

        self.url = "http://localhost:11434/api/embeddings"

        self.headers = {
            "Content-Type": "application/json"
        }

    async def text(self, text: str) -> list[float] | None:
        op: str = "src.ollama.Embeddings.text"

        payload = {
            "model": "nomic-embed-text",
            "prompt": text
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload, headers=self.headers) as response:
                    if response.status == 200:
                        result: dict = await response.json()
                        embedding: list[float] = result.get("embedding", None)

                        return embedding
                    else:
                        log.error(f"API request failed with status {response.status} [{op}]")
                        return None

        except Exception as e:
            log.error(f"Error during API request [{op}] \n{e}")
            raise


text_model = TextModel()
embeddings = Embeddings()
