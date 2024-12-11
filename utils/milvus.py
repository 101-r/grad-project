import hashlib

from pymilvus import MilvusClient

from .logger import log

class Milvus():
    def __init__(self) -> None:
        op: str = "utils.milvus.Milvus.__init__"

        try:
            log.debug(f"Initializing connection to the Milvus vector database [{op}]")
            self.client = MilvusClient(uri="http://localhost:19530", timeout=6.0)

            self.client.using_database("default")
            log.debug("Using 'default' database")

            log.debug("Loading collection into memory")
            self.client.load_collection(collection_name="embeddings")

            log.debug(f"Collection state: {self.client.get_load_state(collection_name="embeddings")}")

        except Exception as e:
            log.error(f"Error initializing Milvus class [{op}] \n{e}")
            raise

    def insert(self, path: str, embedding: list[float], keywords: list[str]) -> None:
        op: str = "utils.milvus.Milvus.insert"

        if len(embedding) != 768:
            raise ValueError(f"Embedding length does not match the schema's dimension [{op}]")

        try:
            data = {
                "id": hashlib.md5(path.encode()).hexdigest(),
                "path": path,
                "embeddings": embedding,
                "keywords": keywords
            }

            self.client.insert(collection_name="embeddings", data=data)

        except Exception as e:
            log.error(f"Error inserting embedding [{op}] \n{e}")
            raise

    def search(self, embedding: list[float]) -> list[list[dict]]:
        op: str = "utils.milvus.Milvus.search"

        try:
            search_params = {
                "metric_type": "IP",
                "params": {"nprobe": 10}
            }

            results = self.client.search(
                collection_name="embeddings",
                data=[embedding],
                anns_field="embeddings",
                search_params=search_params,
                limit=10,
                output_fields=["id", "path"]
            )

            return results

        except Exception as e:
            log.error(f"Error searching [{op}] \n{e}")
            raise

    def close(self) -> None:
        pass


milvus = Milvus()
