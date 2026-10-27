# pip install openai-agents

import asyncio

from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)

# Pas de clé OpenAI réelle : on coupe l'export des traces vers OpenAI
set_tracing_disabled(True)


async def amain() -> None:
    try:
        client = AsyncOpenAI(
            api_key="ollama",
            base_url="http://127.0.0.1:11434/v1",
        )

        model = OpenAIChatCompletionsModel(
            model="gemma4:12b-mlx",
            openai_client=client,
        )

        agent = Agent(
            name="Assistant",
            instructions="Tu es un assistant utile.",
            model=model,
        )

        result = await Runner.run(agent, "Bonjour !")
        print(result.final_output)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(amain())
