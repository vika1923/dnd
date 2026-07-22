from mlx_lm import load, generate

MODEL_NAME = "Qwen/Qwen3-32B-MLX-4bit"

# HISTORY_PATH = "chat_history.json"
# GAME_STATE_PATH = "game_state.json"

MAX_TOKENS = 500

model, tokenizer = load(MODEL_NAME)

def talk_with_agent(conversation_history, new_message, max_tokens=MAX_TOKENS):
    messages = list(conversation_history) + [{"role": "user", "content": new_message}]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, enable_thinking=False
    )
    response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens)
    add_item_to_history("assistant", response, conversation_history)
    return response

def add_item_to_history(role, content, prev_history):
    return prev_history.append({"role": role, "content": content})

if __name__ == "__main__":
    text = talk_with_agent([], "We are playing DnD")
    print(text)