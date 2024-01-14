# @Author: weirdgiser
# @Time: 2024/1/13 21:32
# @Function:
from py2neo import Node
from common.models.neo4j.common import NodeType, RelationType


class GbIndustryNode(NodeType):
    label_type_en = "IndustryGB"
    label_type_zh = "国标行业"
    primary_key = "code"

    label_default_desc = "数据源: 国标行业分类2017"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get("code", None)
        self.name = kwargs.get("name", None)
        self.root_code = kwargs.get("root_code", None)
        self.level = kwargs.get("level", None)
        self.desc = kwargs.get("desc", None)

    def to_neo4j_node(self):
        return Node(self.label_type_en,
                    code=self.code,
                    name=self.name,
                    desc=self.desc,
                    level=self.level,
                    root_code=self.root_code,
                    type=self.label_type_zh)


class DownLevelIndustryRelationship(RelationType):
    type_en = "DOWNLEVEL_INDUSTRY"
    type_zh = "下级行业"


class UpLevelIndustryRelationship(RelationType):
    type_en = "UPLEVEL_INDUSTRY"
    type_zh = "上级行业"
