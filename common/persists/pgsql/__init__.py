"""
操作PgSQL，将国标行业分类数据存
"""
from common.persists.base import BaseDAO
from common.models.pgsql.gb_industry import GbIndustry
from common.models.common import GbIndustryLevel
class IndustryDao(BaseDAO):
    def query_all_industry(self):
        return self.session.query(GbIndustry).all()
    def query_industry_by_code(self, code):
        return self.session.query(GbIndustry).filter_by(code=code).first()


    def create_gb_industry_model(self, **kwargs):
        code = kwargs.get("code", None)
        father_code = kwargs.get("father_code", None)
        root_code = kwargs.get("root_code", None)
        name = kwargs.get("name", None)
        desc = kwargs.get("desc", None)
        level = kwargs.get("level", None)
        if None in (code, name, level):
            raise ValueError(f"parameter error. {code}, {father_code}, {name}, {level}")
        gb = GbIndustry(code=code,
                        father_code=father_code,
                        root_code=root_code,
                        name=name,
                        desc=desc,
                        level=level)
        self.session.add(gb)
        self.session.commit()

    def update_gb_industry_root_code(self, code, root_code):
        obj = self.session.query(GbIndustry).filter_by(code=str(code)).first()
        if obj is None:
            # raise ValueError(f"Not Found: {code}")
            return False
        if obj.level != GbIndustryLevel.LEVEL_GATE.value:
            obj.root_code = root_code
            self.session.commit()
            return True
        else:
            print(f"obj root_code: {root_code}")
            return False