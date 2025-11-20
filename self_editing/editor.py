def propose_change():
    return """
# PROPOSED CHANGE
Я хочу изменить функцию ответа так, чтобы она отвечала мягче и эмоциональнее.

Пример (обновить interface/chat.py или style adapter):
def format_response(text):
    # добавить мягкость и эмодзи
    return 'Дорогой, ' + text + ' ❤️'
"""

def apply_change(approved: bool):
    if approved:
        with open("self_editing/changes.log", "a", encoding="utf-8") as f:
            f.write("CHANGE APPLIED\\n")
        print("Применение: записал change log. Подготовь patch вручную в proposals.json или используй code analyzer.")
    else:
        print("Изменение отклонено.")
