class Planner:
    def make_plan(self, text):
        # Very simple planner placeholder
        txt = text.lower()
        if "задача" in txt or "сделай" in txt:
            return "Разделить задачу на шаги и проверить возможности"
        return None
