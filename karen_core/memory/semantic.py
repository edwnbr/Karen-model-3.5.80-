import os, json
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticMemory:
    def __init__(self):
        self.dir = "data/memory/semantic/"
        os.makedirs(self.dir, exist_ok=True)
        # Lazy init: model will download when first used
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add(self, text):
        emb = self.model.encode(text).tolist()
        eid = str(abs(hash(text)))
        path = os.path.join(self.dir, f"{eid}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"text": text, "embedding": emb}, f, ensure_ascii=False)

    def search(self, query, top_k=3):
        q_emb = self.model.encode(query)
        scores = []
        for f in os.listdir(self.dir):
            data = json.load(open(os.path.join(self.dir, f), "r", encoding="utf-8"))
            emb = np.array(data["embedding"])
            score = float(np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb)))
            scores.append((score, data["text"]))
        scores.sort(reverse=True, key=lambda x: x[0])
        return scores[:top_k]
