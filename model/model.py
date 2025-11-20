from transformers import GPT2Config, GPT2LMHeadModel

def load_model():
    config = GPT2Config(
        n_embd=512,
        n_layer=10,
        n_head=8,
        vocab_size=50257,
    )
    return GPT2LMHeadModel(config)
