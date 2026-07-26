import json
import re
from pathlib import Path

from mlx_lm import load, generate

from dices import roll_dice

MODEL_NAME = "Qwen/Qwen3-32B-MLX-4bit"
MAX_TOKENS = 500
CHAT_HISTORY_FILE = Path(__file__).with_name("chat_history.json")

model, tokenizer = load(MODEL_NAME)

SYSTEM_PROMPT = """
You are the game engine controller for a D&D game.

Decide whether the response needs a tool.

You have access to this function:

1. roll_dice(count, sides)
   - Roll one or more dice.
   - sides must be one of: 4, 6, 8, 10, 12, 20, 100.

If a tool is needed, respond ONLY with JSON:

{
    "function": "roll_dice",
    "arguments": {
        "count": 1,
        "sides": 20
    }
}

If no tool is needed, respond ONLY with JSON:

{
    "function": null,
    "response": "..."
}

Never perform dice rolls yourself.
Never invent dice results.
"""


def _parse_model_decision(response_text):
    cleaned_text = response_text.strip()

    if "</think>" in cleaned_text:
        cleaned_text = cleaned_text.split("</think>", 1)[1].strip()

    match = re.search(r"\{.*\}", cleaned_text, re.S)
    if match is None:
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print("error while parsing json:", e)
        return None


def _extract_response_field(response_text):
    match = re.search(r'"response"\s*:\s*"((?:\\.|[^"\\])*)"', response_text, re.S)
    if match is None:
        return None

    try:
        return json.loads('"{}"'.format(match.group(1)))
    except json.JSONDecodeError:
        return None


def _extract_assistant_response(content):
    if not isinstance(content, str):
        return content

    parsed_content = _parse_model_decision(content)
    if isinstance(parsed_content, dict) and parsed_content.get("function") is None:
        return parsed_content.get("response", content)

    extracted_response = _extract_response_field(content)
    if extracted_response is not None:
        return extracted_response

    return content


def _normalize_history_entry(entry):
    if not isinstance(entry, dict):
        return None

    role = entry.get("role")
    content = entry.get("content")

    if role == "assistant" and isinstance(content, str):
        return {"role": role, "content": _extract_assistant_response(content)}

    if role in {"user", "assistant", "system", "tool"} and "content" in entry:
        return {"role": role, "content": content}

    return None


def _build_prompt(messages, enable_thinking=False):
    return tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
    )


def load_chat_history(history_file=CHAT_HISTORY_FILE):
    if not history_file.exists():
        return []

    try:
        with history_file.open("r", encoding="utf-8") as file_handle:
            history = json.load(file_handle)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(history, list):
        return []

    normalized_history = []
    for entry in history:
        normalized_entry = _normalize_history_entry(entry)
        if normalized_entry is not None:
            normalized_history.append(normalized_entry)

    if normalized_history != history:
        save_chat_history(normalized_history, history_file)

    return normalized_history


def save_chat_history(history, history_file=CHAT_HISTORY_FILE):
    normalized_history = []
    for entry in history:
        normalized_entry = _normalize_history_entry(entry)
        if normalized_entry is not None:
            normalized_history.append(normalized_entry)

    with history_file.open("w", encoding="utf-8") as file_handle:
        json.dump(normalized_history, file_handle, ensure_ascii=False, indent=2)


def talk_with_agent_thinking_disabled(conversation_history, new_message, max_tokens=MAX_TOKENS):
    add_item_to_history("user", new_message, conversation_history)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)

    prompt = _build_prompt(messages, enable_thinking=False)

    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens
    )

    decision = _parse_model_decision(response)
    print("DECISION:", decision)

    if decision is None:
        add_item_to_history("assistant", _extract_assistant_response(response), conversation_history)
        save_chat_history(conversation_history)
        return response

    if decision.get("function") is None:
        assistant_response = _extract_assistant_response(decision.get("response", ""))
        add_item_to_history("assistant", assistant_response, conversation_history)
        save_chat_history(conversation_history)
        return assistant_response


    #########################################################################################
    ################## JSON WAS PARSED => WE ARE CALLING A PYTHON FUNCTION ##################
    #########################################################################################

    if decision.get("function" == "dice_roll"):
        arguments = decision.get("arguments", {})
        count = int(arguments.get("count", 1))
        sides = int(arguments.get("sides", 20))

        tool_result = roll_dice(count, sides)
        final_messages = list(messages)
        final_messages.append({"role": "assistant", "content": response})
        final_messages.append({
            "role": "user",
            "content": (
                "Tool result from roll_dice(count={count}, sides={sides}): {result}. "
                "Use this result to answer the user in plain language."
            ).format(count=count, sides=sides, result=json.dumps(tool_result)),
        })

    final_prompt = _build_prompt(final_messages, enable_thinking=False)
    final_response = generate(
        model,
        tokenizer,
        prompt=final_prompt,
        max_tokens=max_tokens,
    )

    add_item_to_history("assistant", _extract_assistant_response(final_response), conversation_history)
    save_chat_history(conversation_history)
    return final_response



def add_item_to_history(role, content, prev_history):
    if role == "assistant":
        content = _extract_assistant_response(content)
    prev_history.append({"role": role, "content": content})
    return prev_history



if __name__ == "__main__":
    chat_history = load_chat_history()
    text = talk_with_agent_thinking_disabled(
        chat_history,
        "We are playing DnD. I enter the enchanted dark cave. As my eyes are getting used to the darkness, I am screaming to check whether we are alone here",
    )
    print(text)
    print(chat_history)