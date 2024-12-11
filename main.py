import asyncio

from utils.milvus import milvus
from utils.extractor import extractor
from src.ollama import text_model, embeddings

async def main():
    text = extractor.extract_pdf(path="/home/fedora-r/Downloads/grokking-deep-learning.pdf", max_pages=10)

    summary = await text_model.summary(text)

    keywords = extractor.extract_keywords(summary)

    embedding = await embeddings.text(summary)

    milvus.insert("/home/fedora-r/Downloads/grokking-deep-learning.pdf", embedding, keywords)

    query_embedding = await embeddings.text("AI")

    print(milvus.search(query_embedding))


if __name__ == "__main__":
    asyncio.run(main())
