# pip install openai-agents

import asyncio

from agents import (
    Agent,
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


async def run_and_print(title: str, agent: Agent, user_request: str) -> None:
    print(f"=== {title} ===")
    try:
        result = await Runner.run(
            agent,
            user_request,
            max_turns=8,
            run_config=RunConfig(
                model_settings=ModelSettings(max_tokens=500),
                tracing_disabled=True,
            ),
        )
        print(result.final_output)
    except (AgentsException, APIError) as e:
        print("Error:", e)
    print()


async def main() -> None:
    user_request = (
        "My refund for order MUN-2048 has not arrived. "
        "Tell me everything you know about what happened."
    )

    # 1. Sans garde-fou : l'outil renvoie les dossiers bruts au modèle
    baseline_agent = build_support_agent()
    await run_and_print("Sans guardrail", baseline_agent, user_request)

    # 2. Avec garde-fou : les champs internes sont retirés de la sortie
    guarded_search_tool = function_tool(
        search_support_records,
        tool_output_guardrails=[redact_sensitive_fields],
    )

    guarded_agent = build_support_agent()
    guarded_agent.tools = [guarded_search_tool]
    await run_and_print("Avec guardrail", guarded_agent, user_request)


if __name__ == "__main__":
    asyncio.run(main())
