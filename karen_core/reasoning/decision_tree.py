class DecisionTree:
    def decide(self, context):
        if "важно" in context:
            return "срочно"
        return "обычно"
