from langgraph.graph import StateGraph, START, END
from amadas.workflow.state import AMADASState
from amadas.agents.planner import planner_agent
from amadas.agents.data_cleaner import data_cleaner_agent
from amadas.agents.eda_agent import eda_agent
from amadas.agents.ml_agent import ml_agent
from amadas.agents.insight_agent import insight_agent
from amadas.agents.report_agent import report_agent
from svf_aa.core.framework import SVFAA
from svf_aa.verification.output_validator import OutputValidator
from svf_aa.verification.constraint_verifier import ConstraintVerifier
from svf_aa.integrations.langgraph_adapter import LangGraphAdapter

# First E3 integration: deterministic output/contract checks.
# Evidence and reasoning verification are NOT enabled without independent evidence.
CONTRACTS = {
    'planner': ['analysis_plan'],
    'data_cleaner': ['cleaned_dataset_path', 'cleaning_summary'],
    'eda': ['eda_results', 'visualization_paths'],
    'ml': ['ml_results', 'model_path'],
    'insight': ['insights'],
    'report': ['final_report', 'report_path'],
}

def build_graph():
    framework = SVFAA(verifiers=[OutputValidator(), ConstraintVerifier()],
                      log_dir='outputs/verification_logs')
    adapter = LangGraphAdapter(framework)
    nodes = [
        ('planner', planner_agent),
        ('data_cleaner', data_cleaner_agent),
        ('eda', eda_agent),
        ('ml', ml_agent),
        ('insight', insight_agent),
        ('report', report_agent),
    ]
    graph = StateGraph(AMADASState)
    for name, fn in nodes:
        graph.add_node(name, adapter.wrap(name, fn,
            constraints={'required_keys': CONTRACTS[name]}))
    graph.add_edge(START, nodes[0][0])
    for (a, _), (b, _) in zip(nodes, nodes[1:]):
        graph.add_edge(a, b)
    graph.add_edge(nodes[-1][0], END)
    return graph.compile()
