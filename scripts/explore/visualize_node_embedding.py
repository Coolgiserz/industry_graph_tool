# @Author: weirdgiser
# @Time: 2024/1/14 10:26
# @Function:
import os
import pickle

import pandas as pd
from pathlib import Path
import setting
from exploration.node_embedding.visualize import IndustryNodeEmbedding, IndustryVisualizeTool
from common.persists.neo4j.industry import IndustryDAO as IndustryGraphDAO
from common.models.neo4j.industry import GbIndustryNode
from common.persists.redis import RedisClient
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# DATA_DIR = os.path.join(BASE_DIR, "data", "node_embeding","node2vec", "2dim")
DATA_DIR = os.path.join(BASE_DIR, "data", "node_embeding","fastrp", "2dim")

graph_dao = IndustryGraphDAO(uri=setting.neo4j_uri,
                     database=setting.neo4j_db,
                     password=setting.neo4j_pwd)
cached = RedisClient(host=setting.redis_host, port=setting.redis_port, db=2)

def get_node_info_from_neo4j(df_embedding):
    node_embedding_list = []
    # 查询节点信息
    for data in df_embedding.itertuples():
        node_id = getattr(data, "nodeId")
        node_embedding = getattr(data, "embedding")
        # graph_dao.find_node(GbIndustryNode.label_type_en, id)
        result = graph_dao.find_node_by_internal_id(node_id)
        if result is None:
            print(f"nodeId {node_id} not exist.")
            node_embedding_list.append(None)
        else:
            node_name = result.get('name')
            node_level = result.get('level')
            node_code = result.get('code')
            node_root_code = result.get('root_code')
            ine = IndustryNodeEmbedding(id=node_id,
                                        embedding=eval(node_embedding),
                                        name=node_name,
                                        root_code=node_root_code,
                                        code=node_code,
                                        level=node_level
                                        )
            node_embedding_list.append(ine)
    return node_embedding_list
if __name__ == "__main__":
    # 用例
    # cached.flushdb()
    # 读取文件
    data_path= os.path.join(DATA_DIR,"gds.csv")
    print(data_path)
    df_embeding = pd.read_csv(data_path)
    print(df_embeding.shape)
    print(df_embeding.head())
    node_embedding_list_has_cached = "node_embedding_list"
    # 从数据库中查询节点信息
    cache_result = cached.handler.get(node_embedding_list_has_cached)
    if cache_result is None:
        cache_result = get_node_info_from_neo4j(df_embedding=df_embeding)
        cached.handler.set(node_embedding_list_has_cached,
                           pickle.dumps(cache_result)
                           )
    else:
        cache_result = pickle.loads(cache_result)
    assert len(cache_result) == df_embeding.shape[0]
    name_list = []
    code_list = []
    root_code_list = []
    level_list = []
    # 完善df
    for i,data in enumerate(df_embeding.itertuples()):
        name_list.append(cache_result[i].name)
        code_list.append(cache_result[i].code)
        root_code_list.append(cache_result[i].root_code)
        level_list.append(cache_result[i].level)
    df_embeding["name"] = name_list
    df_embeding["level"] = level_list
    df_embeding["code"] = code_list
    df_embeding["root_code"] = root_code_list
    vt = IndustryVisualizeTool(dataframe=df_embeding)
    vt.plot_2d_scatter()
    print("Done!")

