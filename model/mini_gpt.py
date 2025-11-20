from transformers import GPT2Config, GPT2LMHeadModel

def load_mini_gpt():
    config = GPT2Config(
        n_embd=768,
        n_layer=12,
        n_head=12,
        vocab_size=50257,
    )
    return GPT2LMHeadModel(config)
