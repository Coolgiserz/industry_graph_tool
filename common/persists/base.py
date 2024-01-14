import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class BaseDAO:
    def __init__(self, connect_str, session=None):
        # pool_recycle=900,每15分钟重建连接（无效）
        # 参考官方文档的连接池配置：https://docs.sqlalchemy.org/en/20/core/pooling.html
        #  pool_size=20, max_overflow=0
        self.engine = create_engine(connect_str, pool_size=20, max_overflow=0, pool_recycle=900)
        if session is not None:
            self.session = session
        else:
            self.session = sessionmaker(self.engine)()
        assert isinstance(self.session, sqlalchemy.orm.session.Session)
