# @Author: weirdgiser
# @Time: 2024/1/13 21:01
# @Function:
#
#    国标行业知识图谱
#    图数据库构建
#
import tqdm

import setting
from common.persists.neo4j.industry import IndustryDAO as IndustryGraphDAO
from common.persists.pgsql import IndustryDao as IndustryPgDAO

def main():
    graph_dao = IndustryGraphDAO(uri=setting.neo4j_uri,
                     database=setting.neo4j_db,
                     password=setting.neo4j_pwd)
    pg_dao = IndustryPgDAO(connect_str=setting.get_connect_string())
    industrys = pg_dao.query_all_industry()
    for industry in tqdm.tqdm(industrys):
        industry_node = graph_dao.merge_industry_node(code=industry.code,
                                      root_code=industry.root_code,
                                      name=industry.name,
                                      level=industry.level,
                                      desc=industry.desc,)
        if industry.father_code is not None:
            # 构建上下级行业节点关系
            father_industry_node = pg_dao.query_industry_by_code(code=industry.father_code)
            father_industry_node = graph_dao.merge_industry_node(code=father_industry_node.code,
                                      root_code=father_industry_node.root_code,
                                      name=father_industry_node.name,
                                      level=father_industry_node.level,
                                      desc=father_industry_node.desc)
            graph_dao.merge_industry_relation(uplevel_node=father_industry_node, downlevel_node=industry_node)


if __name__ == "__main__":
    main()