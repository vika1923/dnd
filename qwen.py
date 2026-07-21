from mlx_lm import load, generate

model, tokenizer = load("Qwen/Qwen3-32B-MLX-4bit")
messages = [{"role": "user", "content": "Write a story about Einstein"}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

text = generate(model, tokenizer, prompt=prompt, verbose=True)
