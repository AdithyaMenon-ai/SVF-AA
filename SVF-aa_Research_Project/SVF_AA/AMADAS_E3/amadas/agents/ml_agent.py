from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.multiclass import type_of_target

from amadas.workflow.state import AMADASState


def ml_agent(state: AMADASState) -> dict:
    print('[ML] Training model')
    target = state.get('target_column') or state['analysis_plan'].get('target_column')
    if not target or state['analysis_plan'].get('ml_task') == 'not_applicable':
        return {'ml_results': {'status': 'skipped', 'reason': 'No suitable ML task'}, 'model_path': None}
    df = pd.read_csv(state['cleaned_dataset_path'])
    if target not in df.columns:
        return {'ml_results': {'status': 'skipped', 'reason': 'Target not found'}, 'model_path': None}
    X = df.drop(columns=[target]).dropna(axis=1, how='all')
    y = df[target]
    if X.empty or len(df) < 20 or y.nunique() < 2:
        return {'ml_results': {'status': 'skipped', 'reason': 'Insufficient usable data'}, 'model_path': None}
    kind = type_of_target(y)
    if kind in ('binary', 'multiclass') and (not pd.api.types.is_numeric_dtype(y) or y.nunique() <= 20):
        task = 'classification'
        model = LogisticRegression(max_iter=1000)
        counts = y.value_counts()
        stratify = y if counts.min() >= 2 and len(counts) <= int(len(y) * 0.2) else None
    elif kind == 'continuous':
        task = 'regression'
        model = Ridge()
        stratify = None
    else:
        return {'ml_results': {'status': 'skipped', 'reason': f'Unsupported target type: {kind}'}, 'model_path': None}
    numeric = X.select_dtypes(include='number').columns.tolist()
    categorical = X.columns.difference(numeric).tolist()
    transforms = []
    if numeric:
        transforms.append(('numeric', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
        ]), numeric))
    if categorical:
        transforms.append(('categorical', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore')),
        ]), categorical))
    preprocess = ColumnTransformer(transforms)
    pipeline = Pipeline([('preprocess', preprocess), ('model', model)])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    if task == 'classification':
        metrics = {
            'accuracy': round(float(accuracy_score(y_test, predictions)), 4),
            'f1_weighted': round(float(f1_score(y_test, predictions, average='weighted', zero_division=0)), 4),
        }
    else:
        metrics = {
            'mae': round(float(mean_absolute_error(y_test, predictions)), 4),
            'r2': round(float(r2_score(y_test, predictions)), 4),
        }
    model_path = Path('outputs/models') / f'{state["task_id"]}_model.joblib'
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    return {'ml_results': {
        'status': 'completed', 'task': task, 'model': type(model).__name__,
        'train_rows': len(X_train), 'test_rows': len(X_test), 'metrics': metrics,
        'target_column': target,
    }, 'model_path': str(model_path)}
