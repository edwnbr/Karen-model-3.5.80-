import os, json, uuid, time
class EpisodicMemory:
    def __init__(self):
        self.dir = "data/memory/episodic/"
        os.makedirs(self.dir, exist_ok=True)

    def add(self, text):
        eid = str(uuid.uuid4())
        path = os.path.join(self.dir, f"{eid}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"text": text, "ts": time.time()}, f, ensure_ascii=False)

    def get_recent(self, count=5):
        files = sorted(os.listdir(self.dir), reverse=True)
        results = []
        for f in files[:count]:
            with open(os.path.join(self.dir, f), "r", encoding="utf-8") as fh:
                results.append(json.load(fh)["text"])
        return results
