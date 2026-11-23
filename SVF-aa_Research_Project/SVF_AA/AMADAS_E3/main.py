import argparse
import json
import time
from pathlib import Path
from uuid import uuid4

from amadas.workflow.graph import build_graph


def main():
    parser = argparse.ArgumentParser(description='AMADAS E3 verified prototype')
    parser.add_argument('--dataset', default='datasets/raw/iris.csv')
    parser.add_argument('--target', default='target')
    parser.add_argument('--query', default='Analyze the Iris dataset and build a classification model.')
    args = parser.parse_args()
    task_id = str(uuid4())
    state = {
        'task_id': task_id, 'user_query': args.query,
        'dataset_path': args.dataset, 'target_column': args.target or None,
        'execution_logs': [], 'errors': [],
    }
    print('AMADAS — E3 SVF-AA Integration')
    graph = build_graph()
    started = time.perf_counter()
    logs = []
    try:
        for event in graph.stream(state, stream_mode='updates'):
            for node, update in event.items():
                logs.append({'node': node, 'updated_fields': list(update)})
                state.update(update)
        status = 'completed'
        print('Report:', state['report_path'])
        print('Model:', state.get('model_path'))
        print('Plots:', state.get('visualization_paths', []))
    except Exception as exc:
        status = 'failed'
        state.setdefault('errors', []).append(f'{type(exc).__name__}: {exc}')
        print('Experiment failed:', state['errors'][-1])
        raise
    finally:
        record = {
            'experiment': 'E3', 'task_id': task_id, 'status': status,
            'elapsed_seconds': round(time.perf_counter() - started, 3),
            'steps': logs, 'errors': state.get('errors', []),
            'ml_results': state.get('ml_results'),
            'report_path': state.get('report_path'),
        }
        log_path = Path('outputs') / f'{task_id}_execution.json'
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(record, indent=2, default=str), encoding='utf-8')
        print('Execution log:', log_path)


if __name__ == '__main__':
    main()
