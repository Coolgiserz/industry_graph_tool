import os
import unittest
from configparser import ConfigParser
from industry_parser.tool import GBIndustry2017Parser
from setting import config_parser
source_dir = config_parser.get("data", "dir")
source_file = config_parser.get("data", "filename")
source_data = os.path.join(source_dir, source_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

class TestIndustryParser(unittest.TestCase):
    def setUp(self) -> None:
        self.gb_parser = GBIndustry2017Parser(xlsx_path=source_data)
    def test_parse_major_industry(self):
        # Use a breakpoint in the code line below to debug your script.

        self.gb_parser._parse_gb_category()
        res_A= self.gb_parser._get_major_industry(code="A")
        # print(res)
        res_B = self.gb_parser._get_major_industry(code="B")
        # print(gb_parser._get_major_industry(code="B"))
        # print(gb_parser.df.iloc[746])

    def test_get_root_gb_industry(self):
        test_cases = ["A", "01","05","2140","6853","900","786"]
        for case in test_cases:
            root_obj = self.gb_parser.get_root_gb_industry(case)
            print(f"Case {case}: {root_obj}")

if __name__ == '__main__':
    unittest.main()
