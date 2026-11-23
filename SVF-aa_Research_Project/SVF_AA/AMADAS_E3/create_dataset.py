from pathlib import Path
from sklearn.datasets import load_iris

path = Path('datasets/raw/iris.csv')
path.parent.mkdir(parents=True, exist_ok=True)
load_iris(as_frame=True).frame.to_csv(path, index=False)
print('Created', path)
