import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from config.config import get_config
from src.ado_client import AzureDevOpsClient
from src.query_parser import parse_question
from src.metrics import calculate_metrics
from src.ai_gateway import generate_ai_analysis
from src.report_generator import build_executive_report


load_dotenv()

st.set_page_config(
    page_title="Azure DevOps AI Delivery Insights",
    page_icon="📊",
    layout="wide",
)

st.title("Azure DevOps AI Delivery Insights")

st.caption(
    "System Analysis POC — Natural Language → ADO Data → "
    "Delivery Metrics → AI Gateway → Executive Insights"
)

config = get_config()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("Data Source")

    data_mode = st.radio(
        "Select data source",
        [
            "Demo Data",
            "Client Azure DevOps",
        ],
    )

    st.divider()

    st.header("AI Analysis")

    ai_mode = st.radio(
        "Select AI mode",
        [
            "Local Demo AI",
            "Client AI Gateway",
        ],
    )

    st.divider()

    st.info(
        "Demo Data and Local Demo AI require no credentials."
    )


# ---------------------------------------------------------
# QUESTION
# ---------------------------------------------------------

st.subheader("Ask a Delivery Question")

question = st.text_area(
    "Natural language question",
    value="What has Team A completed in the last 60 days?",
    height=100,
)


st.write("### Example Questions")

examples = [
    "What has Team A completed in the last 60 days?",
    "How is Team B performing this sprint?",
    "Show delivery risks for Platform Team.",
    "Summarise completed Epics this quarter.",
    "What are the blockers affecting Team A?",
]

cols = st.columns(5)

for index, example in enumerate(examples):

    if cols[index].button(
        example,
        use_container_width=True,
    ):
        question = example


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if st.button(
    "Analyse Delivery Performance",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a question.")

        st.stop()

    with st.spinner("Analysing delivery performance..."):

        try:

            # ---------------------------------------------
            # STEP 1 — INTENT
            # ---------------------------------------------

            intent = parse_question(question)

            # ---------------------------------------------
            # STEP 2 — DATA SOURCE
            # ---------------------------------------------

            if data_mode == "Client Azure DevOps":

                client = AzureDevOpsClient(
                    organization_url=config["ado_url"],
                    project=config["ado_project"],
                    pat=config["ado_pat"],
                )

                df = client.query_work_items(intent)

                source_label = "Client Azure DevOps"

            else:

                sample_path = (
                    Path(__file__).parent
                    / "data"
                    / "sample_ado_data.csv"
                )

                df = pd.read_csv(sample_path)

                source_label = "Sample ADO Data"

            # ---------------------------------------------
            # STEP 3 — FILTER
            # ---------------------------------------------

            filtered = df.copy()

            if intent.get("team"):

                team_name = intent["team"].lower()

                filtered = filtered[
                    filtered["Team"]
                    .astype(str)
                    .str.lower()
                    == team_name
                ]

            # ---------------------------------------------
            # DATE FILTER
            # ---------------------------------------------

            if intent.get("days"):

                if "ClosedDate" in filtered.columns:

                    closed_dates = pd.to_datetime(
                        filtered["ClosedDate"],
                        errors="coerce",
                    )

                    cutoff = (
                        pd.Timestamp.today().normalize()
                        - pd.Timedelta(
                            days=int(intent["days"])
                        )
                    )

                    filtered = filtered[
                        (closed_dates >= cutoff)
                        | closed_dates.isna()
                    ]

            # ---------------------------------------------
            # EMPTY RESULT
            # ---------------------------------------------

            if filtered.empty:

                st.warning(
                    "No matching work items were found."
                )

                st.stop()

            # ---------------------------------------------
            # STEP 4 — METRICS
            # ---------------------------------------------

            metrics = calculate_metrics(filtered)

            # ---------------------------------------------
            # STEP 5 — AI ANALYSIS
            # ---------------------------------------------

            ai_result = generate_ai_analysis(
                metrics=metrics,
                question=question,
                gateway_url=(
                    config["ai_gateway_url"]
                    if ai_mode == "Client AI Gateway"
                    else ""
                ),
                gateway_key=(
                    config["ai_gateway_key"]
                    if ai_mode == "Client AI Gateway"
                    else ""
                ),
                model=config["ai_model"],
            )

            # ---------------------------------------------
            # STEP 6 — REPORT
            # ---------------------------------------------

            report = build_executive_report(
                metrics,
                ai_result,
            )

            st.success(
                f"Analysis completed using {source_label}."
            )

            # ---------------------------------------------
            # METRICS
            # ---------------------------------------------

            st.subheader("Delivery Metrics")

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            col1.metric(
                "Stories",
                metrics["stories_completed"],
            )

            col2.metric(
                "Bugs Resolved",
                metrics["bugs_resolved"],
            )

            col3.metric(
                "Tasks",
                metrics["tasks_completed"],
            )

            col4.metric(
                "PRs",
                metrics["prs_merged"],
            )

            col5.metric(
                "Cycle Time",
                f'{metrics["avg_cycle_time"]:.1f} days',
            )

            col6.metric(
                "Blocked",
                metrics["blocked_items"],
            )

            st.divider()

            # ---------------------------------------------
            # EXECUTIVE SUMMARY
            # ---------------------------------------------

            left, right = st.columns([1.2, 1])

            with left:

                st.subheader("Executive Summary")

                st.write(
                    report["executive_summary"]
                )

                st.subheader(
                    "Delivery Highlights"
                )

                for item in report["highlights"]:

                    st.markdown(
                        f"✓ {item}"
                    )

                st.subheader("Risks")

                for item in report["risks"]:

                    st.markdown(
                        f"⚠ {item}"
                    )

                st.subheader(
                    "Recommendations"
                )

                for item in report["recommendations"]:

                    st.markdown(
                        f"**{item}**"
                    )

            # ---------------------------------------------
            # METRIC TABLE
            # ---------------------------------------------

            with right:

                st.subheader(
                    "Performance Overview"
                )

                overview = {

                    "Total Work Items":
                        metrics["total_items"],

                    "Completed Items":
                        metrics["completed_items"],

                    "Stories Completed":
                        metrics["stories_completed"],

                    "Bugs Resolved":
                        metrics["bugs_resolved"],

                    "Tasks Completed":
                        metrics["tasks_completed"],

                    "PRs Merged":
                        metrics["prs_merged"],

                    "Average Cycle Time":
                        round(
                            metrics["avg_cycle_time"],
                            1,
                        ),

                    "Average Lead Time":
                        round(
                            metrics["avg_lead_time"],
                            1,
                        ),

                    "Blocked Items":
                        metrics["blocked_items"],

                    "High Priority Items":
                        metrics[
                            "high_priority_items"
                        ],
                }

                overview_df = pd.DataFrame(
                    overview.items(),
                    columns=[
                        "Metric",
                        "Value",
                    ],
                )

                st.dataframe(
                    overview_df,
                    hide_index=True,
                    use_container_width=True,
                )

            # ---------------------------------------------
            # WORK ITEMS
            # ---------------------------------------------

            st.subheader(
                "Work Items Used in Analysis"
            )

            st.dataframe(
                filtered,
                hide_index=True,
                use_container_width=True,
            )

            # ---------------------------------------------
            # SYSTEM ANALYSIS
            # ---------------------------------------------

            with st.expander(
                "System Analysis — Parsed Intent"
            ):

                st.json(intent)

            # ---------------------------------------------
            # AI RESPONSE
            # ---------------------------------------------

            with st.expander(
                "AI Gateway Response"
            ):

                st.json(ai_result)

        except Exception as exc:

            st.error(
                "The analysis could not be completed."
            )

            st.exception(exc)

else:

    st.info(
        "Select Demo Data + Local Demo AI for an immediate "
        "zero-credential walkthrough."
    )
