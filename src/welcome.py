import os
import asyncio
from typing import List
from openai import AsyncOpenAI


client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def welcome_texts(name: str) -> List[str]:
    """Welcome texts."""
    texts = [
        (
            f"@{name} привет! Расскажи пожалуйста немного о себе и "
            "что смотивировало тебя присоединиться к симулятору?"
        ),
        (
            f"Привет! @{name}.\nУ нас тут есть традиция. Каждый, кто подключается, "
            "рассказывает, как они дошли до жизни с ML-симулятором."
        ),
        (
            f"@{name}, приветствую от лица всех участников группы! Мы рады, "
            "что ты теперь с нами.\n"
            "И у нас для тебя уже есть первое задание. "
            "Расскажи, пожалуйста, немного о себе и что тебя привело к нам."
        ),
    ]
    return texts


def welcome_prompt(name: str) -> str:
    """Build prompt using input texts."""
    examples = "\n\n\n".join(welcome_texts(name))
    prompt = f"""
    Сгенерируй приветственное гендерно-нейтральное сообщение для пользователя @{name}.

    За основу возьми эти сообщения:
    {examples}
    """
    return prompt


async def openai_response(name: str) -> str:
    """Generating a greeting using GPT-3.5-turbo."""
    response = await client.chat.completions.create(
        messages=[
            {"role": "user", "content": welcome_prompt(name)},
        ],
        model="gpt-3.5-turbo",
        temperature=0.75,
    )
    choice, *_ = response.choices
    return choice.message.content  # type: ignore


async def main() -> None:
    welcome_message = await openai_response("username")
    print(welcome_message)


if __name__ == "__main__":
    asyncio.run(main())
