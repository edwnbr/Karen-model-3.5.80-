from transformers import Trainer, TrainingArguments, AutoTokenizer, GPT2LMHeadModel
from datasets import Dataset
import json, os

data_file = 'training/dialogues.jsonl'
if not os.path.exists(data_file):
    print('No dialogues dataset found at', data_file)
    exit(0)

tokenizer = AutoTokenizer.from_pretrained('gpt2')
samples=[]
with open(data_file,'r',encoding='utf-8') as f:
    for line in f:
        samples.append(json.loads(line))

texts = [s['prompt'] + '\n' + s['response'] for s in samples]
enc = tokenizer(texts, truncation=True, padding=True, max_length=512)
ds = Dataset.from_dict(enc)

# Load existing trained model if exists, otherwise small config
if os.path.exists('./trained_model'):
    model = GPT2LMHeadModel.from_pretrained('./trained_model')
else:
    model = GPT2LMHeadModel.from_pretrained('gpt2')

training_args = TrainingArguments(
    output_dir='./ft_out',
    num_train_epochs=1,
    per_device_train_batch_size=2,
    save_total_limit=2
)

trainer = Trainer(model=model, args=training_args, train_dataset=ds)
trainer.train()
trainer.save_model('./ft_model')
print("Fine-tune complete. Saved to ./ft_model")
