import os, json
class LongTermMemory:
    def __init__(self):
        self.file = "data/memory/long_term.json"
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        if not os.path.exists(self.file):
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add(self, text):
        with open(self.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append(text)
        if len(data) > 1000:
            data = data[-1000:]
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_all(self):
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)
