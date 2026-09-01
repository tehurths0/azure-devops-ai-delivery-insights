# azure-devops-ai-delivery-insights
AI-powered Proof of Concept for Azure DevOps delivery performance analysis and executive insights.
azure-devops-ai-delivery-insights/
│
├── README.md
│
├── app.py
├── requirements.txt
├── .env.example
│
├── data/
│   └── sample_azure_devops_data.csv
│
├── src/
│   ├── data_loader.py
│   ├── metrics.py
│   ├── insights.py
│   └── recommendations.py
│
├── tests/
│   └── test_metrics.py
│
├── docs/
│   ├── system-analysis.md
│   └── architecture.md
│
└── screenshots/
    └── dashboard.png
How to run the demo
Download/clone this repository.
Install Python 3.11+.
Run pip install -r requirements.txt.
Run python app.py.
Open the displayed local URL.
No coding is required.
requirements.txt
┌──────────────────────────────────────────────┐
│       Azure DevOps AI Delivery Insights      │
├──────────────────────────────────────────────┤
│ Team:        [Team A ▼]                      │
│ Period:      [Last 60 Days ▼]                │
│                                              │
│ Ask a question:                              │
│ [ What has Team A completed in the last     │
│   60 days?                              ]     │
│                                              │
│              [ Generate Insights ]            │
├──────────────────────────────────────────────┤
│ Executive Summary                            │
│                                              │
│ ✓ 42 items completed                         │
│ ✓ Average cycle time: 5.2 days              │
│ ✓ Delivery trend: +18%                      │
│                                              │
│ AI Recommendations                           │
│ • ...                                         │
└──────────────────────────────────────────────┘
