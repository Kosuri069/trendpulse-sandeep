# TrendPulse

TrendPulse is a 4-step Python data pipeline project that collects trending stories from the Hacker News API, cleans the data, analyzes patterns, and creates visualizations.

## Project Overview

This project is built as a sequence of four tasks:

- **Task 1:** Fetch top Hacker News stories and save them as JSON
- **Task 2:** Clean the JSON data and save it as CSV
- **Task 3:** Analyze the cleaned data using Pandas and NumPy
- **Task 4:** Visualize the results using Matplotlib

Each task uses the output of the previous one.

## Project Structure

```text
trendpulse-yourname/
│
├── task1_data_collection.py
├── task2_data_processing.py
├── task3_analysis.py
├── task4_visualization.py
├── README.md
│
├── data/
│   ├── trends_YYYYMMDD.json
│   ├── cleaned_trends.csv
│   ├── category_summary.csv
│   ├── top_authors.csv
│   ├── top_stories.csv
│   └── analysis_summary.txt
│
└── outputs/
    ├── posts_by_category.png
    ├── avg_score_by_category.png
    ├── top_authors.png
    └── score_distribution.png
