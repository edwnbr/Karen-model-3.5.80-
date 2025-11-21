import os
import openai
from dotenv import load_dotenv
from karen.style_adapter import load_or_build_profile, apply_style_to_text
from karen_core.memory.short_term import ShortTermMemory
from karen_core.memory.long_term import LongTermMemory
from karen_core.memory.episodic import EpisodicMemory
from karen_core.memory.semantic import SemanticMemory
from karen_core.nlp.text_processor import TextProcessor
from karen_core.utils.logger import Logger
from karen_core.self_update.updater import Updater
from karen_core.reasoning.planner import Planner

# Загружаем ключ из .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Brain:
    def __init__(self):
        self.logger = Logger()
        self.short_mem = ShortTermMemory()
        self.long_mem = LongTermMemory()
        self.episodic_mem = EpisodicMemory()
        self.semantic_mem = SemanticMemory()
        self.text_proc = TextProcessor()
        self.updater = Updater()
        self.planner = Planner()
        self.style_profile = load_or_build_profile()

    def get_gpt5_reply(self, user_text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-5-mini",
                messages=[{"role": "user", "content": user_text}]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"[Ошибка GPT]: {e}"

    def run(self):
        print("Karen AI запущена. Привет, Женя!")
        while True:
            try:
                user_input = input("Ты: ")
            except (KeyboardInterrupt, EOFError):
                print("\nВыход.")
                break

            processed = self.text_proc.process(user_input)

            # Сохраняем в память
            self.short_mem.add(processed)
            self.episodic_mem.add(processed)
            self.long_mem.add(processed)
            self.semantic_mem.add(processed)

            # Генерация ответа через GPT
            raw_reply = self.get_gpt5_reply(processed)
            reply = apply_style_to_text(raw_reply, self.style_profile, user_name="Женя")
            print(reply)
            self.logger.log_conversation(user_input, reply)

            # Планирование
            plan = self.planner.make_plan(processed)
            if plan:
                print(f"[Karen] План действий: {plan}")

            # Проверка предложений изменений кода
            proposal = self.updater.check_for_proposals()
            if proposal:
                print(f"[Karen] Предложение изменения кода:\n{proposal['description']}")
                accept = input("Применяем? (да/нет): ")
                if accept.strip().lower() in ("да", "y", "yes"):
                    self.updater.apply_change(proposal)
