import asyncio
import json

# лимит на длину статьи
TEXT_LIMIT = 5000
CHUNK_SIZE = 3000

def text_processing(filename: str) -> str:
    with open(filename, encoding="utf-8") as text_file:
        raw_text = text_file.read()
        if len(raw_text) > 3400:
            chunks = [raw_text[index: index + CHUNK_SIZE] for index in range(0, len(raw_text), CHUNK_SIZE)]
            text = "\n".join([f"Часть {index + 1}\n{chunk}" for index, chunk in enumerate(chunks)])
        else:
            text = raw_text
        text += '\n\nКонец'
        return text


def create_prompt(text: str, filename: str) -> list[str]:
    with open(filename, encoding="utf-8") as prompt_file:
        prompt = prompt_file.read()
    prompt += (
        f"Сократи итоговый получившийся текст, длина статьи не должна превышать {TEXT_LIMIT} "
        f"символов (например, из каждого абзаца можно исключить незначимые, лишние предложения, либо переформулировать "
        f"мысль абзаца более коротко). Вот поэтому сначала необходимо всё выслушать. Если длина получившейся статьи больше, "
        f"чем ты можешь написать за одно сообщение, я буду ждать продолжение в следующем твоём сообщении."
    )
    prompt += "\n\n" + text
    chunks = prompt.split("Часть")
    prompts = [chunks[0].strip() + "\nЧасть " + chunks[1].strip()]
    if len(chunks) > 1:
        prompts += ["\nЧасть " + chunks[i] for i in range(2, len(chunks))]
    return prompts

