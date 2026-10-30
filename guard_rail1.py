import json

from agents import (
    ToolGuardrailFunctionOutput,
    ToolOutputGuardrailData,
    tool_output_guardrail,
)

SENSITIVE_FIELDS = {
    "internal_refund_token",
    "fraud_risk_score",
    "internal_case_assessment",
}


@tool_output_guardrail
def redact_sensitive_fields(
    data: ToolOutputGuardrailData,
) -> ToolGuardrailFunctionOutput:
    records = json.loads(data.output)

    for record in records:
        for field_name in SENSITIVE_FIELDS:
            record.pop(field_name, None)

    sanitized_output = json.dumps(
        records,
        ensure_ascii=False,
    )

    # reject_content remplace la sortie de l'outil par ce message
    # avant qu'elle ne soit transmise au modèle
    return ToolGuardrailFunctionOutput.reject_content(
        sanitized_output
    )
