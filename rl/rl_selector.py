import random
from db.chroma_setup import collection
def rl_version(base_name: str, epsilon: float = 0.1):
    result = collection.get(where={"base_name": base_name})
    if not result or "metadatas" not in result:
        print(f"No version data found for base name: {base_name}")
        return None
    reward_scores = []
    for meta in result["metadatas"]:
        reward_scores.append(meta.get("reward_score", 0))
    if not reward_scores:
        print("No reward scores found for versions.")
        return None
    if random.random() < epsilon:
        selected_index = random.randint(0, len(reward_scores) - 1)
    else:
        selected_index = reward_scores.index(max(reward_scores))
    return {
        "id": result["ids"][selected_index],
        "document": result["documents"][selected_index],
        "metadata": result["metadatas"][selected_index]
    }
