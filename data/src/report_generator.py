def build_executive_report(
    metrics: dict,
    ai_result: dict,
) -> dict:

    return {

        "executive_summary":
            ai_result.get(

                "executive_summary",

                (
                    f'{metrics["completed_items"]} '
                    "work items were completed "
                    "in the selected scope."
                ),

            ),

        "highlights":
            ai_result.get(
                "highlights",
                [],
            ),

        "risks":
            ai_result.get(
                "risks",
                [],
            ),

        "recommendations":
            ai_result.get(
                "recommendations",
                [],
            ),

    }
