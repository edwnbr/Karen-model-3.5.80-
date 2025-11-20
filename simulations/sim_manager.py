import json
import time
import random
import os

SIM_DIR = "simulations/simulations_data"
os.makedirs(SIM_DIR, exist_ok=True)

class Mission:
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or {}

    def run(self):
        t = random.uniform(0.05, 0.2)
        time.sleep(t)
        score = random.random()
        return {"mission": self.name, "score": score, "params": self.params}

class SimManager:
    def __init__(self):
        self.missions = []

    def add_mission(self, name, params=None):
        m = Mission(name, params)
        self.missions.append(m)
        return m

    def run_all(self):
        results = []
        for m in self.missions:
            res = m.run()
            results.append(res)
            path = os.path.join(SIM_DIR, f"{m.name}_{int(time.time())}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False)
        return results

if __name__ == '__main__':
    sm = SimManager()
    sm.add_mission('optimize_dialog_style', {'target': 'warmth'})
    print(sm.run_all())
