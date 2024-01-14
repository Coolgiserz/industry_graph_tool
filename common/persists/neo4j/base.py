# @Author: weirdgiser
# @Time: 2024/1/13 21:20
# @Function:
from py2neo import Graph, Node, Relationship, NodeMatcher

class BaseDAO(object):
    def __init__(self, uri, database, password):
        self.graph = Graph(uri, auth=(database, password))

    def run_query(self, cypher, parameters=None, **kwargs):
        """
        执行原声Cypher
        """
        return self.graph.run(cypher, parameters, **kwargs)

    def create_node(self, label, **properties):
        """
        CREATE节点
        """
        node = Node(label, **properties)
        self.graph.create(node)
        return node

    def merge_relationship(self, node1, rel_type, node2, *primary_key, **properties):
        rel = Relationship(node1, rel_type, node2, **properties)
        self.graph.merge(rel, rel_type, *primary_key)
        return rel

    def merge_node(self, label, *primary_key, **properties):
        """
        MERGE节点
        """
        node = Node(label,  **properties)
        self.graph.merge(node, label, *primary_key)
        return node

    def find_all_node(self, label, **properties):
        return self.graph.nodes.match(label, **properties).all()

    def find_node(self, label, **properties):
        return self.graph.nodes.match(label, **properties).first()

    def find_relationship(self, r_type, **properties):
        return self.graph.relationships.match(None, r_type, **properties)

    def find_node_by_internal_id(self, node_id):
        cypher = f"MATCH (n) WHERE ID(n)={node_id} RETURN n"
        result = self.run_query(cypher).data()
        if len(result)>0:
            return result[0]["n"]
        else:
            return None
