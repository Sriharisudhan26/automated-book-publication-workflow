from db.chroma_setup import collection
def score_updation(base_name: str, version_id: str, new_score: float, alpha: float = 0.2):
    results = collection.get(where={"base_name": base_name})
    if not results or version_id not in results["ids"]:
        print(f"Version ID {version_id} not found under base_name: {base_name}")
        return
    index = results["ids"].index(version_id)
    metadata = results["metadatas"][index]
    current_score = metadata.get("reward_score", 0)
    updated_score = round((1 - alpha) * current_score + alpha * new_score, 2)
    collection.update(
        ids=[version_id],
        metadatas=[{
            **metadata,
            "reward_score": updated_score
        }]
    )

    print(f"Updated score for version {version_id}: {current_score} → {updated_score}")
