from typing import Any, TypedDict


class AMADASState(TypedDict, total=False):
    task_id: str
    user_query: str
    dataset_path: str
    target_column: str | None
    analysis_plan: dict[str, Any]
    cleaned_dataset_path: str
    cleaning_summary: dict[str, Any]
    eda_results: dict[str, Any]
    visualization_paths: list[str]
    ml_results: dict[str, Any]
    model_path: str | None
    insights: list[str]
    final_report: str
    report_path: str
    execution_logs: list[dict[str, Any]]
    errors: list[str]
