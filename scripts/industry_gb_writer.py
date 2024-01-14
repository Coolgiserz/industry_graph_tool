import tqdm

import entities
import setting
import pickle
from common.persists.pgsql import IndustryDao
from common.persists.redis import RedisClient
cached = RedisClient(host=setting.redis_host,
                     port=setting.redis_port,
                     db=setting.redis_db)

level_mapping = {
    entities.GBIndustry.GATE_CATEGORY: 0,
    entities.GBIndustry._MAJOR_CATEGORY: 1,
    entities.GBIndustry._MEDIUM_CATEGORY: 2,
    entities.GBIndustry._SMALL_CATEGORY: 3,
}

def get_gb_obj(code):
    value = cached.handler.get(code)
    if value is None:
        return None
    gb_obj = pickle.loads(value)
    return gb_obj

def calc_root_code(code):
    """
    计算行业的根行业编码
    """
    value = cached.handler.get(code)
    if value is None:
        return False
    gb_obj = pickle.loads(value)
    assert isinstance(gb_obj, entities.GBIndustry)
    if gb_obj.gb_type == entities.GBIndustry.GATE_CATEGORY:
        # 门类行业本身即是根节点
        return gb_obj
    else:
        return calc_root_code(gb_obj.father_code)

def batch_update_root_code():
    dao = IndustryDao(connect_str=setting.get_connect_string())
    all_industry_keys = cached.handler.keys('*')
    print(f"key len: {len(all_industry_keys)}")
    count = 0
    for key in tqdm.tqdm(all_industry_keys):
        gb_obj = get_gb_obj(code=key)
        print(gb_obj)
        if gb_obj is not None:
            root_gb_obj = calc_root_code(key)
            print(f"root: {root_gb_obj}")
            dao.update_gb_industry_root_code(gb_obj.gb_code, root_code=root_gb_obj.gb_code)
    print(count)

def main():
    dao = IndustryDao(connect_str=setting.get_connect_string())
    all_industry_keys = cached.handler.keys('*')
    print(f"key len: {len(all_industry_keys)}")
    count = 0
    for key in tqdm.tqdm(all_industry_keys):
        value = cached.handler.get(key)
        res = pickle.loads(value)
        print(key, res)
        if res is not None:
            assert isinstance(res, entities.GBIndustry)
            dao.create_gb_industry_model(code=res.gb_code,
                                         father_code=res.father_code,
                                         name=res.gb_name,
                                         level=level_mapping.get(res.gb_type),
                                         desc=res.desc
                                         )
            count += 1
    print(f"失败条数: {len(all_industry_keys)-count}")



if __name__ == "__main__":
    batch_update_root_code()