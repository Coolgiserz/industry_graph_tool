# @Author: weirdgiser
# @Time: 2024/1/13 21:24
# @Function:
from common.persists.neo4j.base import BaseDAO
from common.models.neo4j.industry import GbIndustryNode, DownLevelIndustryRelationship, UpLevelIndustryRelationship
class IndustryDAO(BaseDAO):
    def merge_industry_node(self, code, **kwargs):
        """
        """
        name = kwargs.get("name", None)
        root_code = kwargs.get("root_code", None)
        desc = kwargs.get("desc", None)
        level = kwargs.get("level", None)

        gb_industry_node = GbIndustryNode(name=name,
                                          code=code,
                                          desc=desc,
                                          root_code=root_code,
                                          level=level)
        self.graph.merge(gb_industry_node.to_neo4j_node(),
                         gb_industry_node.get_label_type(),
                         gb_industry_node.get_primary_key())
        return self.find_node(gb_industry_node.get_label_type(),code=code)

    def merge_industry_relation(self, uplevel_node, downlevel_node):
        self.merge_relationship(uplevel_node, DownLevelIndustryRelationship.type_en, downlevel_node, comment=DownLevelIndustryRelationship.type_zh)

