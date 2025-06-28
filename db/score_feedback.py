from db.chroma_setup import collection

def update_score(base_name: str, final_version: str, new_score: float):
    results = collection.get(where={"base_name": base_name})
    if not results:
        print("No versions found for:", base_name)
        return
    for i, doc in enumerate(results["documents"]):
        if doc.strip() == final_version.strip():
            doc_id = results["ids"][i]
            collection.update(
                ids=[doc_id],
                metadatas=[{"reward_score": new_score}]
            )
            print(f"Score updated for version {doc_id} to {new_score}")
            return
    print("Final version not found")
