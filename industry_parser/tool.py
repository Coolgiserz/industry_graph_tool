import os.path
import pickle
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from utils.logtool import create_logger
import pandas as pd
import string
from entities import GBIndustry
from utils.redis_client import RedisClient
uppercase_letters = string.ascii_uppercase
cache = RedisClient()
logger = create_logger("industry_parser", console=True, logfilename=os.path.join(BASE_DIR, "logs", "log.log"))
class IndustryParser(object):
    pass



def dataframe_column_isin(dataframe, field_name, isin_list):
    assert isinstance(dataframe, pd.DataFrame)
    return dataframe[dataframe[field_name].isin(isin_list)]
class GBIndustry2017Parser(IndustryParser):
    """
    国标行业分类2017解析
    1. 解析门类：门类编号、门类介绍、门类名称、门类索引起止
    2. 解析大类：大类所属门类编号，大类编号、大类介绍、大类名称、大类索引起止
    3. 解析中类：中类所属大类编号、中类编号、

    TODO: 图书介绍
    """
    _COLUMN_1 = "column1"
    _COLUMN_2 = "column2"
    _COLUMN_3 = "column3"
    _COLUMN_4 = "column4"

    _COLUMN_COMMENT = "comment"
    def __init__(self, xlsx_path):
        self.df = pd.read_excel(xlsx_path)
        logger.info(f"read {xlsx_path}, shape: {self.df.shape}, {self.df.shape[0]}")
        self.index_max = self.df.shape[0]-1
        self.df.columns = [GBIndustry2017Parser._COLUMN_1, GBIndustry2017Parser._COLUMN_2, GBIndustry2017Parser._COLUMN_3,GBIndustry2017Parser._COLUMN_4,GBIndustry2017Parser._COLUMN_COMMENT]
        self.code_to_gb_category = {}
        self.code_to_gb_major_industry = {}
        self.code_to_gb_medium_industry = {}
        self.code_to_gb_small_industry = {}


    def run(self):
        logger.info("========start running parser!=====")

        # 处理国标行业门类
        logger.info(f"====处理国标行业门类（三位数）")

        self._parse_gb_category()
        #
        logger.info(f"code_to_gb_category len: {self.code_to_gb_category}")

        # 处理国标行业大类
        logger.info(f"====处理国标行业大类（三位数）")

        self._parse_gb_major_industry()
        # TODO 处理国标行业中类
        logger.info(f"code_to_gb_major_industry len: {self.code_to_gb_major_industry}")
        logger.info(f"====处理国标行业中类（三位数）")
        logger.info(f"code_to_gb_medium_industry len: {self.code_to_gb_medium_industry}")

        self._parse_gb_medium_industry()
        logger.info(f"====处理国标行业小类（四位数）")
        logger.info(f"code_to_gb_small_industry len: {self.code_to_gb_small_industry}")

        # TODO 处理国标行业小类
        for code, gb_small_category in self.code_to_gb_medium_industry.items():
            self.get_industry_by_code(code, gb_type=GBIndustry._SMALL_CATEGORY, gb=gb_small_category)

    def get_root_gb_industry(self, code):
        """
        获取根行业编码
        """
        value = cache.handler.get(code)
        if value is None:
            return False
        gb_obj = pickle.loads(value)
        assert isinstance(gb_obj, GBIndustry)
        if gb_obj.gb_type == GBIndustry.GATE_CATEGORY:
            # 门类行业本身即是根节点
            return gb_obj
        else:
            return self.get_root_gb_industry(gb_obj.father_code)

    def get_industry_by_code(self, code: str, gb_type: str,  gb):
        """
        如果级别的国标小类，则
        :param code:
        :param level:
        :return:
        """
        logger.info(f"---process code customed mode {code}")

        df_industry_temp = self.df.iloc[gb.index_start:gb.index_end + 1]
        logger.info(f"df_industry_temp shape: {df_industry_temp.shape}")
        # 解析国标行业 xx
        # df_major_industry[df_major_industry[GBIndustry2017Parser._COLUMN_1].notnull()]
        industrys = None
        column = GBIndustry2017Parser._COLUMN_1
        if gb_type == GBIndustry._SMALL_CATEGORY:
            column = GBIndustry2017Parser._COLUMN_2
            industrys = df_industry_temp[df_industry_temp[column].fillna('').astype(str).str.len() == 4]
            if industrys.shape[0] == 0:
                logger.error(f"++++ {code}")
        assert isinstance(industrys, pd.DataFrame)
        index_list = industrys.index.to_list()
        index_list.append(gb.index_end)
        logger.info(f"industrys shape:{industrys.shape}")
        logger.info(f"index_list:{index_list}")
        for i, industry in enumerate(industrys.itertuples()):
            # logger.info(f"-----processing {industry}")
            code_i = getattr(industry, column)

            index_start = index_list[i]
            index_end = index_list[i + 1] - 1
            desc = self.df[GBIndustry2017Parser._COLUMN_4].iloc[index_start + 1]
            name = getattr(industry, GBIndustry2017Parser._COLUMN_4)
            gb = GBIndustry(index_start=index_start,
                            index_end=index_end,
                            gb_name=name,
                            gb_code=code_i,
                            father_code=code,
                            gb_type=gb_type,
                            desc=desc)
            logger.info(f"gb {code_i}: {gb}")
            self.code_to_gb_small_industry[code_i] = gb
            cache.handler.set(code_i, pickle.dumps(gb))

    def _get_major_industry(self, code):
        gb = self.code_to_gb_category[code]
        logger.info(f"---process code {code} ,{gb}")

        #
        df_major_industry = self.df.iloc[gb.index_start:gb.index_end+1]
        logger.info(f"df_major_industry shape: {df_major_industry.shape}")
        # 解析国标行业大类 xx
        # df_major_industry[df_major_industry[GBIndustry2017Parser._COLUMN_1].notnull()]
        # 要加上.astype(str)，否则从O开始的数据类型为int导致df_major_industry[GBIndustry2017Parser._COLUMN_1].str.len()==2]无法命中
        major_industrys = df_major_industry[df_major_industry[GBIndustry2017Parser._COLUMN_1].fillna('').astype(str).str.len()==2]
        assert isinstance(major_industrys, pd.DataFrame)
        if major_industrys.shape[0] == 0:
            logger.error(f"{df_major_industry.iloc[0].values}")
        index_list = major_industrys.index.to_list()
        index_list.append(gb.index_end)
        # logger.info(f"major industry: {major_industrys}")
        logger.info(f"major_industrys shape:{major_industrys.shape}")

        logger.info(f"index_list:{index_list}")
        for i, major_industry in enumerate(major_industrys.itertuples()):
            # logger.info(f"-----processing {major_industry}")
            major_code = getattr(major_industry, GBIndustry2017Parser._COLUMN_1)
            index_start = index_list[i]
            index_end = index_list[i+1]-1
            desc = self.df[GBIndustry2017Parser._COLUMN_4].iloc[index_start+1]
            name =  getattr(major_industry, GBIndustry2017Parser._COLUMN_4)
            gb = GBIndustry(index_start=index_start,
                            index_end=index_end,
                            gb_name=name,
                            gb_code=major_code,
                            father_code=code,
                            gb_type=GBIndustry._MAJOR_CATEGORY,
                            desc=desc)
            logger.info(f"gb: {gb}")
            self.code_to_gb_major_industry[major_code] = gb
            cache.handler.set(major_code, pickle.dumps(gb))

    def _get_medium_industry(self, code):
        """
        解析国标行业中类
        - 获取起止索引
        :param code:
        :return:
        """
        logger.info(f"-------process medium_industry code {code}")
        gb = self.code_to_gb_major_industry[code]
        df_medium_industry = self.df.iloc[gb.index_start:gb.index_end + 1]
        logger.info(f"df_medium_industry shape: {df_medium_industry.shape}")
        # 需要加.fillna('')，否则nan转成str后长度也是3
        medium_industrys = df_medium_industry[df_medium_industry[GBIndustry2017Parser._COLUMN_1].fillna('').astype(str).str.len() == 3]
        assert isinstance(medium_industrys, pd.DataFrame)
        index_list = medium_industrys.index.to_list()
        index_list.append(gb.index_end)
        logger.info(f"medium_industrys shape:{medium_industrys.shape}")

        logger.info(f"medium_industrys index_list:{index_list}")
        for i, medium_industry in enumerate(medium_industrys.itertuples()):
            medium_code = getattr(medium_industry, GBIndustry2017Parser._COLUMN_1)
            logger.info(f"-----processing {medium_code}")

            index_start = index_list[i]
            index_end = index_list[i + 1] - 1
            desc = self.df[GBIndustry2017Parser._COLUMN_4].iloc[index_start + 1]
            name = getattr(medium_industry, GBIndustry2017Parser._COLUMN_4)
            gb = GBIndustry(index_start=index_start,
                            index_end=index_end,
                            gb_name=name,
                            gb_code=medium_code,
                            father_code=code,
                            gb_type=GBIndustry._MEDIUM_CATEGORY,
                            desc=desc)
            logger.info(f"gb medium: {gb}")
            self.code_to_gb_medium_industry[medium_code] = gb
            cache.handler.set(medium_code, pickle.dumps(gb))
    def _parse_gb_category(self):
        # 解析国标行业门类
        res = dataframe_column_isin(self.df, GBIndustry2017Parser._COLUMN_1, list(uppercase_letters) )
        index_list = res.index.to_list()
        index_list.append(self.index_max)
        # print(len(index_list),index_list)
        for i, data in enumerate(res.itertuples()):
            # 国标行业门类描述
            code = getattr(data, GBIndustry2017Parser._COLUMN_1)
            index_start = index_list[i]
            index_end = index_list[i+1]-1
            desc = self.df[GBIndustry2017Parser._COLUMN_4].iloc[index_start+1]
            name =  self.df[GBIndustry2017Parser._COLUMN_4].iloc[index_start]
            gb = GBIndustry(index_start=index_start,
                            index_end=index_end,
                            gb_name=name,
                            gb_code=code,
                            father_code=None,
                            gb_type=GBIndustry.GATE_CATEGORY,
                            desc=desc)
            self.code_to_gb_category[code] = gb
            logger.info(f"gb gate: {gb}")

            # 存储入库
            cache.handler.set(code, pickle.dumps(gb))



    def _parse_gb_major_industry(self):
        """
        解析国标行业大类
        :return:
        """
        for code, gb_category in self.code_to_gb_category.items():
            self._get_major_industry(code=code)

    def _parse_gb_medium_industry(self):
        for code, gb_medium_category in self.code_to_gb_major_industry.items():
            self._get_medium_industry(code)