from pathlib import Path
import pandas as pd

from amadas.workflow.state import AMADASState


def data_cleaner_agent(state: AMADASState) -> dict:
    print('[CLEANER] Cleaning dataset')
    df = pd.read_csv(state['dataset_path'])
    target = state.get('target_column') or state['analysis_plan'].get('target_column')
    if target and target not in df.columns:
        raise ValueError(f'Target column not found: {target}')
    before = len(df)
    missing_before = {k: int(v) for k, v in df.isna().sum().items()}
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    missing_target = int(df[target].isna().sum()) if target else 0
    if target:
        df = df.dropna(subset=[target])
    # Deliberately leave feature missing values untouched. The ML pipeline
    # fits imputation on training data only to avoid test-set leakage.
    output = Path('datasets/processed') / f'{state["task_id"]}_cleaned.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    summary = {
        'original_rows': before,
        'cleaned_rows': len(df),
        'columns': len(df.columns),
        'duplicates_removed': duplicates,
        'rows_missing_target_removed': missing_target,
        'missing_before': missing_before,
        'missing_after': {k: int(v) for k, v in df.isna().sum().items()},
        'feature_missing_values_deferred_to_ml_pipeline': True,
    }
    return {'cleaned_dataset_path': str(output), 'cleaning_summary': summary}
