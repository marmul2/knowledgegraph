from py2neo import Graph, Node, Relationship
from typing import Dict, List, Tuple

class KnowledgeGraphBuilder:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.graph = Graph(uri, auth=(user, password))
        
    def create_entity_node(self, entity: Dict) -> Node:
        """创建实体节点"""
        node = Node(entity["label"],
                   name=entity["text"],
                   start=entity["start"],
                   end=entity["end"])
        self.graph.create(node)
        return node
    
    def create_relationship(self, start_node: Node, rel_type: str, end_node: Node):
        """创建关系"""
        rel = Relationship(start_node, rel_type, end_node)
        self.graph.create(rel)
        
    def build_graph(self, entities: List[Dict], relationships: List[Tuple]):
        """构建知识图谱"""
        # 清空现有图谱
        self.graph.delete_all()
        
        # 创建实体节点
        nodes = {}
        for entity in entities:
            node = self.create_entity_node(entity)
            nodes[entity["text"]] = node
            
        # 创建关系
        for rel in relationships:
            if rel[0] in nodes and rel[2] in nodes:
                self.create_relationship(nodes[rel[0]], rel[1], nodes[rel[2]])