import unittest
import redis
import pickle
class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.r = redis.StrictRedis(host="localhost",port=6379, db=0)
    def get(self, code):
        res = self.r.get(code)
        if res is not None:
            obj = pickle.loads(res)
            print(f"obj: {obj}")
        else:
            print("None!")
    def test_something(self):
        print(self.r.get("ok"))
        print(self.r.get("123"))
        print(self.r.get("B"))
        codes = ["R", "C", "01", "10", "30", "693", "0111"]
        for code in codes:
            obj = self.get(code)
            # print(obj)

    def test_small_industry_parser(self):

        codes = ["R", "86", "861", "8610", "8621",8621, "Q", "781","786","7869"]
        for code in codes:
            self.get(code)


if __name__ == '__main__':
    unittest.main()
