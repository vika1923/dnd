from mlx_lm import load, generate
import json
import os
from datetime import datetime

model, tokenizer = load("Qwen/Qwen3-32B-MLX-4bit")
messages = [{"role": "user", "content": "Write a story about Einstein"}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

text = generate(model, tokenizer, prompt=prompt, verbose=True)

assistant_message = {"role": "assistant", "content": text}
messages.append(assistant_message)

# Persist chat history to a JSON file. Each run appends a new entry with a timestamp.
history_path = "chat_history.json"
entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "messages": messages,
}

# Load existing history (if any) then append and save back.
history = []
if os.path.exists(history_path):
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        # If the file is corrupted or unreadable, start fresh.
        history = []

history.append(entry)

with open(history_path, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

print(f"Chat saved to {history_path}")
