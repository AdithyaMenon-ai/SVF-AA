from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from amadas.workflow.state import AMADASState


def eda_agent(state: AMADASState) -> dict:
    print('[EDA] Computing statistics and plots')
    df = pd.read_csv(state['cleaned_dataset_path'])
    numeric = df.select_dtypes(include='number')
    summary = df.describe(include='all').replace({float('inf'): None, float('-inf'): None})
    summary = summary.astype(object).where(pd.notna(summary), None)
    corr = numeric.corr().round(4) if len(numeric.columns) > 1 else pd.DataFrame()
    plot_dir = Path('outputs/plots') / state['task_id']
    plot_dir.mkdir(parents=True, exist_ok=True)
    plots = []
    if not numeric.empty:
        axes = numeric.hist(figsize=(10, 7), bins=15)
        fig = axes.flatten()[0].figure
        fig.tight_layout()
        path = plot_dir / 'distributions.png'
        fig.savefig(path, dpi=140)
        plt.close(fig)
        plots.append(str(path))
    if not corr.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        image = ax.imshow(corr.to_numpy(), vmin=-1, vmax=1, cmap='coolwarm')
        ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
        ax.set_yticks(range(len(corr.index)), corr.index)
        fig.colorbar(image, ax=ax)
        fig.tight_layout()
        path = plot_dir / 'correlations.png'
        fig.savefig(path, dpi=140)
        plt.close(fig)
        plots.append(str(path))
    results = {
        'shape': [int(df.shape[0]), int(df.shape[1])],
        'columns': df.columns.tolist(),
        'missing_values': {k: int(v) for k, v in df.isna().sum().items()},
        'descriptive_statistics': summary.to_dict(),
        'correlations': corr.to_dict() if not corr.empty else {},
    }
    return {'eda_results': results, 'visualization_paths': plots}
