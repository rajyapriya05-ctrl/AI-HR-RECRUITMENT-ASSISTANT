from typing import Callable, Dict, Any, List


class Node:
    def __init__(self, name: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.name = name
        self.fn = fn

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.fn(state)


class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, a: str, b: str):
        self.edges.append((a, b))

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        for n in self.nodes:
            out = n.run(state)
            if out:
                state.update(out)
        return state
