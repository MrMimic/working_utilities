import networkx as nx


class Graph(object):
    """
    Directed graph processing
    """

    def __init__(self):
        pass

    def initiate_graph(self, graph_type):
        """
        """
        if graph_type == 'digraph':
            return nx.DiGraph()

    def add_edge(self, graph, source, target, weight):
        """
        """
        graph.add_edge(str(source), str(target), weight=weight)
        return graph

    def get_successors(self, graph, node):
        """
        """
        return [x for x in graph.successors(node)]

    def get_predecessors(self, graph, node):
        """
        """
        return [x for x in graph.predecessors(node)]

    def get_edge_weight(self, graph, source, target):
        """
        """
        weight = graph.get_edge_data(source, target)
        if weight is not None:
            return weight['weight']
        else:
            return None

    def get_possible_starts(self, graph):
        """
        """
        possible_starts = []
        for node in graph.nodes():
            if len(list(graph.predecessors(node))) == 0:
                possible_starts.append(node)
        return possible_starts

    def get_distance(self, graph, node_1, node_2):
        """Get mean distance between two points"""
        path_length = nx.shortest_path_length(
            graph, source=node_1, target=node_2)
        return path_length

    def set_edge_weight(self, graph, source, target, weight):

        graph[source][target]['weight'] = weight
        return graph
