import os
import time
from chromadb import PersistentClient
chroma_client = PersistentClient(path=os.path.join(os.getcwd(), "chroma"))
collection = chroma_client.get_or_create_collection(name="chapter_versions")
def version_storage(content: str, base_name: str, version_type: str, score: float, extra_metadata: dict = None):
    metadata = {
        "base_name": base_name,
        "version_type": version_type,
        "reward_score": score
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    doc_id = f"{base_name}_{version_type}_{int(time.time())}"
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"✅ Version stored in ChromaDB: {doc_id}")
def get_latest_version(base_name: str, version_type: str = "raw"):
    results = collection.get(
        where={"base_name": base_name, "version_type": version_type},
        limit=1,
        include=["documents", "metadatas", "ids"]
    )
    if results and results.get("documents"):
        return results["documents"][0]
    return None
def list_versions(base_name: str):
    results = collection.get(
        where={"base_name": base_name},
        include=["documents", "metadatas", "ids"]
    )
    return results

