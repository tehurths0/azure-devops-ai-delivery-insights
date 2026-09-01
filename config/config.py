import os


def get_config():

    return {

        "ado_url":
            os.getenv(
                "ADO_URL",
                ""
            ).strip(),

        "ado_project":
            os.getenv(
                "ADO_PROJECT",
                ""
            ).strip(),

        "ado_pat":
            os.getenv(
                "ADO_PAT",
                ""
            ).strip(),

        "ai_gateway_url":
            os.getenv(
                "AI_GATEWAY_URL",
                ""
            ).strip(),

        "ai_gateway_key":
            os.getenv(
                "AI_GATEWAY_KEY",
                ""
            ).strip(),

        "ai_model":
            os.getenv(
                "AI_MODEL",
                ""
            ).strip(),

    }
