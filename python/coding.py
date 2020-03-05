from typing import Any, List, Tuple
import networkx as nx
import matplotlib.pyplot as plt


class InheritenceGraphe():

    def __init__(self, base_class: Any, graph_path: str = None):

        if graph_path is None:
            self.graph_path: str = f"{self.clean_class_str(base_class)}_inheritence_graph.png"
        else:
            self.graph_path: str = graph_path

        self.digraph = nx.DiGraph()
        self.to_treat: List[Any] = [base_class]
        self.edges: List[Tuple] = list()

        self.build_edges()
        self.draw_graphe()

    def get_children_classes(self, cls):
        return cls.__subclasses__()

    def clean_class_str(self, cls):
        return str(cls).replace("'>", "").split(".")[-1]

    def build_edges(self):
        while len(self.to_treat) > 0:
            children = self.get_children_classes(self.to_treat[0])
            if len(children) > 0:
                self.to_treat = self.to_treat + children

            for child in children:
                self.edges.append(
                    (
                        self.clean_class_str(self.to_treat[0]),
                        self.clean_class_str(child)
                    )
                )

            del self.to_treat[0]

    def draw_graphe(self):
        self.digraph.add_edges_from(self.edges)
        plt.figure(figsize=(16, 9))
        param = {
            "with_labels": True,
            "node_color": "#F5DCD6",
            "arrows": True,
            "arrowsize": 8,
            "linewidths": .8,
            "edge_color": "#F4927C",
            "font_size": 12,
            "font_weight": "bold",
            "alpha": 1
        }
        nx.draw_kamada_kawai(self.digraph, **param)
        plt.savefig(self.graph_path)
