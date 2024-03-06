class GBIndustry(object):
    GATE_CATEGORY = "门类"
    _MAJOR_CATEGORY = "大类"
    _MEDIUM_CATEGORY = "中类"
    _SMALL_CATEGORY = "小类"

    def __init__(self, **kwargs):
        self.gb_type = kwargs.pop("gb_type", None)
        self.gb_name = kwargs.get("gb_name", None)
        self.gb_code = kwargs.get("gb_code", None)
        self.father_code = kwargs.get("father_code", None)
        self.desc = kwargs.get("desc", None)

        self.index_start = kwargs.get("index_start", None)
        self.index_end = kwargs.get("index_end", None)

    def __str__(self):
        return f"GBIndustry(code={self.gb_code},name={self.gb_name},desc={self.desc},start={self.index_start},end={self.index_end},father_code={self.father_code})"