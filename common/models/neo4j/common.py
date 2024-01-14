# @Author: weirdgiser
# @Time: 2024/1/13 21:29
# @Function:

# 节点标签
class NodeType(object):
    label_type_en = "COMMON_NODE"
    label_type_zh = "通用节点"
    primary_key = "id"

    def __init__(self, **kwargs):
        # 节点名称
        self.name = kwargs.pop("name", None)
        # 节点
        self.type = kwargs.pop("type", None)

    def get_label_type(self):
        return self.label_type_en

    def get_primary_key(self):
        return self.primary_key

    def to_neo4j_node(self):
        raise NotImplementedError("must be implemented by subclass.")


class VirtualNodeType(NodeType):
    """
    虚拟节点
    """
    label_type_en = "VIRTUAL_NODE"
    label_type_zh = "虚拟节点"


class RelationType(object):
    type_zh = "通用关系"
    type_en = "COMMON_RELATION"
    primary_key = "id"


class NodeEmbeddingType:
    def __init__(self, **kwargs):
        self.node_id = kwargs.get("id")
        self.embeding = kwargs.get("embedding")
        self.name = kwargs.get("name", self.node_id)


    def get_dim(self):
        return len(self.embeding)