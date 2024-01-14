# coding: utf-8
from sqlalchemy import Column, Integer, String, Text, Time, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GbIndustry(Base):
    __tablename__ = 'gb_industry'
    __table_args__ = {'comment': '国标行业分类表'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('gb_industry_id_seq'::regclass)"), comment='自增长ID')
    updated_at = Column(Time(True), server_default=text("CURRENT_TIMESTAMP"), comment='数据更新时间')
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, comment='国标行业编码（2017）')
    father_code = Column(String, comment='上级行业编码')
    root_code = Column(String, comment='一级行业编码')
    desc = Column(Text, comment='描述')
    level = Column(Integer, comment='行业级别：门类0，大类1，中类2，小类3')
