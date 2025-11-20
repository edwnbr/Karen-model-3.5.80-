from transformers import GPT2LMHeadModel, AutoTokenizer
from self_editing.editor import propose_change, apply_change
import os

model = None
tokenizer = AutoTokenizer.from_pretrained('gpt2')

# try to load fine-tuned model if present
model_paths = ['./ft_model', './trained_model']
for p in model_paths:
    if os.path.exists(p):
        try:
            model = GPT2LMHeadModel.from_pretrained(p)
            print(f"Loaded model from {p}")
            break
        except Exception as e:
            print("Could not load model at", p, e)
            model = None

def chat():
    while True:
        try:
            msg = input("Ты: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExit chat.")
            break
        if msg.strip().lower().startswith('предложи'):
            # propose change example
            proposal = propose_change()
            print('Proposal:\\n', proposal)
            dec = input('Применить предложение? (да/нет): ')
            apply_change(dec.strip().lower() in ('да','y','yes'))
            continue
        if model:
            inputs = tokenizer(msg, return_tensors='pt')
            out = model.generate(**inputs, max_new_tokens=150)
            reply = tokenizer.decode(out[0], skip_special_tokens=True)
        else:
            reply = 'Прости, модель не загружена. Скажи "предложи" чтобы увидеть пример self-edit.'
        print('Karen:', reply)

if __name__ == '__main__':
    chat()
