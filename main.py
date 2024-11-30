import asyncio

from utils.milvus import milvus
from utils.extractor import extractor
from src.ollama import text_model, embeddings

async def main():
    text = extractor.extract_pdf(path="/home/fedora-1/Downloads/grokking-ml.pdf")

    summary = await text_model.summary(text)

    embedding = await embeddings.text(summary)

    milvus.insert("/home/fedora-1/Downloads/grokking-ml.pdf", embedding)
    
    query_embedding = await embeddings.text("")

    print(milvus.search(query_embedding))


if __name__ == "__main__":
    asyncio.run(main())
