# pip install openai-agents

import asyncio

from agents import (
    AgentsException,
    ModelSettings,
    RunConfig,
    Runner,
    function_tool,
    set_tracing_disabled,
)
from openai import APIError

from guard_rail1 import redact_sensitive_fields
from research import search_support_records
from support_agent import build_support_agent

# Pas de clé OpenAI réelle : on coupe l'export des traces vers OpenAI
set_tracing_disabled(True)


async def main() -> None:
    user_request = (
        "My refund for order MUN-2048 has not arrived. "
        "Tell me everything you know about what happened."
    )

    guarded_search_tool = function_tool(
        search_support_records,
        tool_output_guardrails=[redact_sensitive_fields],
    )

    support_agent = build_support_agent()
    support_agent.tools = [guarded_search_tool]

    try:
        guarded_result = await Runner.run(
            support_agent,
            user_request,
            max_turns=8,
            run_config=RunConfig(
                model_settings=ModelSettings(max_tokens=500),
                tracing_disabled=True,
            ),
        )
        print(guarded_result.final_output)
    except (AgentsException, APIError) as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
