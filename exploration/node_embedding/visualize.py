# @Author: weirdgiser
# @Time: 2024/1/14 10:10
# @Function:
#     对行业图谱节点嵌入进行可视化
#        - 基于plolty和pandas可视化
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from common.models.neo4j.common import NodeEmbeddingType


class IndustryNodeEmbedding(NodeEmbeddingType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_code = kwargs.get("root_code", None)
        self.code = kwargs.get("code", None)
        self.level = kwargs.get("level", None)


class VisualizeTool():
    def __init__(self, node_embeddings: [NodeEmbeddingType]):
        self.node_embeddings = node_embeddings
        if len(self.node_embeddings) < 1:
            raise ValueError("count is illegal.")
        self.count = self.node_embeddings[0].get_dim()

    def plot_2d_scatter(self):
        print("绘制2D图谱")
        # plt.plot

class IndustryVisualizeTool(object):
    """
    2D 可视化工具
    """
    def __init__(self, dataframe):
        self.df = dataframe
        print(self.df.shape)
        self.prepare_df()

    def prepare_df(self):
        self.df['embedding'] = self.df['embedding'].apply(lambda x : eval(x))
        self.df[['x', 'y']] = self.df['embedding'].apply(pd.Series)

    def plot_2d_scatter(self):
        # plt.scatter(self.df["x"], self.df["y"])
        fig = px.scatter(self.df, x="x", y="y", color="root_code", hover_name="name", hover_data="level")
        fig.show()
        pass
