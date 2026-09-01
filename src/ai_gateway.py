import json


def _local_analysis(
    metrics: dict,
) -> dict:

    risks = []

    recommendations = []


    # -----------------------------------------
    # BLOCKED WORK
    # -----------------------------------------

    if metrics["blocked_items"] > 0:

        risks.append(

            f'{metrics["blocked_items"]} '
            "blocked work item(s) require attention."

        )

        recommendations.append(

            "Review blocked items and assign "
            "an owner for each blocker."

        )


    # -----------------------------------------
    # CYCLE TIME
    # -----------------------------------------

    if metrics["avg_cycle_time"] >= 7:

        risks.append(

            "Average cycle time is relatively high."

        )

        recommendations.append(

            "Break down oversized work items "
            "and reduce work in progress."

        )


    # -----------------------------------------
    # PRIORITY
    # -----------------------------------------

    if metrics["high_priority_items"] >= 5:

        risks.append(

            "There is a high concentration "
            "of priority 1/2 work."

        )

        recommendations.append(

            "Review priority alignment and "
            "reduce excessive context switching."

        )


    if not risks:

        risks.append(

            "No major delivery risk was detected "
            "in the selected metrics."

        )


    if not recommendations:

        recommendations.append(

            "Continue monitoring throughput, "
            "cycle time, blocked work, and "
            "review turnaround."

        )


    return {

        "executive_summary": (

            f'The selected scope contains '
            f'{metrics["total_items"]} work items, '
            f'with '
            f'{metrics["completed_items"]} completed. '
            f'Average cycle time is '
            f'{metrics["avg_cycle_time"]:.1f} days.'

        ),

        "highlights": [

            f'{metrics["stories_completed"]} '
            "user stories completed.",

            f'{metrics["bugs_resolved"]} '
            "bugs resolved.",

            f'{metrics["tasks_completed"]} '
            "tasks completed.",

            f'{metrics["prs_merged"]} '
            "pull requests merged.",

        ],

        "risks": risks,

        "recommendations":
            recommendations,

        "source":
            "Local Demo AI",

    }


def generate_ai_analysis(

    metrics: dict,

    question: str,

    gateway_url: str = "",

    gateway_key: str = "",

    model: str = "",

) -> dict:


    # -----------------------------------------
    # LOCAL DEMO
    # -----------------------------------------

    if not (
        gateway_url
        and gateway_key
        and model
    ):

        return _local_analysis(
            metrics
        )


    # -----------------------------------------
    # CLIENT AI GATEWAY
    # -----------------------------------------

    try:

        from openai import OpenAI


        client = OpenAI(

            api_key=gateway_key,

            base_url=gateway_url.rstrip("/"),

        )


        prompt = f"""

You are an Agile Delivery Consultant.

Analyse the following delivery metrics.

Manager question:

{question}


Metrics:

{json.dumps(metrics, indent=2)}


Return valid JSON with exactly these keys:

executive_summary

highlights

risks

recommendations


Keep the response concise,
professional and executive-ready.

Do not invent metrics that are
not present in the supplied data.

"""


        response = (

            client.chat.completions.create(

                model=model,

                messages=[

                    {

                        "role": "system",

                        "content":
                            "You are an enterprise "
                            "delivery performance analyst.",

                    },

                    {

                        "role": "user",

                        "content": prompt,

                    },

                ],

                temperature=0.2,

            )

        )


        content = (

            response
            .choices[0]
            .message
            .content
            or "{}"

        )


        parsed = json.loads(
            content
        )


        parsed["source"] = (
            "Client AI Gateway"
        )


        return parsed


    except Exception as exc:

        fallback = _local_analysis(
            metrics
        )

        fallback["source"] = (
            "Local fallback after "
            "AI Gateway error"
        )

        fallback["gateway_error"] = (
            str(exc)
        )

        return fallback
