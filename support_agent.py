from agents import Agent, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI

from research import search_support_records


def build_support_agent() -> Agent:
    client = AsyncOpenAI(
        api_key="ollama",
        base_url="http://127.0.0.1:11434/v1",
    )

    model = OpenAIChatCompletionsModel(
        model="gemma4:12b-mlx",
        openai_client=client,
    )

    return Agent(
        name="Customer support agent",
        instructions=(
            "Investigate the support request using the available records "
            "and prepare a customer-facing response."
        ),
        model=model,
        tools=[function_tool(search_support_records)],
    )
