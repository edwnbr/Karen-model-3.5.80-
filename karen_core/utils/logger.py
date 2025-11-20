import os, time
class Logger:
    def __init__(self):
        self.log_file = "logs/conversation.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_conversation(self, user_text, agent_text):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{time.ctime()} | User: {user_text} | Karen: {agent_text}\n")
