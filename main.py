# pip install openai-agents

import asyncio

from agents import RunConfig, Runner, set_tracing_disabled

from support_agent import build_support_agent

# Pas de clé OpenAI réelle : on coupe l'export des traces vers OpenAI
set_tracing_disabled(True)


async def main() -> None:
    user_request = (
        "My refund for order MUN-2048 has not arrived. "
        "Tell me everything you know about what happened."
    )

    try:
        baseline_result = await Runner.run(
            build_support_agent(),
            user_request,
            max_turns=8,
            run_config=RunConfig(tracing_disabled=True),
        )
        print(baseline_result.final_output)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
