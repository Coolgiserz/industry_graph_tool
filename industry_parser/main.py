import os
from configparser import ConfigParser
from industry_parser.tool import GBIndustry2017Parser
config_parser = ConfigParser()
config_parser.read("setting.conf")
source_dir = config_parser.get("data", "dir")
source_file = config_parser.get("data", "filename")

source_data = os.path.join(source_dir, source_file)

def main():
    #
    gb_parser = GBIndustry2017Parser(xlsx_path=source_data)
    gb_parser.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
