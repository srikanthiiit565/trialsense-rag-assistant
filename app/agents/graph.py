"""Agent graph orchestration."""

from langgraph.graph import StateGraph

from app.agents.state import AgentState

from app.agents.nodes import (

	retrieve_node,

	rerank_node,

	build_context_node,

	answer_node,

)


graph = StateGraph(AgentState)

graph.add_node(

	"retrieve",

	retrieve_node,

)

graph.add_node(

	"rerank",

	rerank_node,

)

graph.add_node(

	"context",

	build_context_node,

)

graph.add_node(

	"answer",

	answer_node,

)

graph.set_entry_point("retrieve")

graph.add_edge(

	"retrieve",

	"rerank",

)

graph.add_edge(

	"rerank",

	"context",

)

graph.add_edge(

	"context",

	"answer",

)

graph.set_finish_point("answer")

rag_graph = graph.compile()
