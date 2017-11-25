import unittest
from UnitTest.widget import WidGet


class WidGetTestCase(unittest.TestCase):
    """setUp 和 tearDown 函数在每个测试方法前后运行"""
    def setUp(self):
        self.widget = WidGet()

    def tearDown(self):
        self.widget.dispose()
        self.widget = None

    # specify the unit test's order through special function name
    def test_1size(self):
        self.assertEqual(self.widget.get_size(), (40, 40))

    def test_2resize(self):
        self.widget.resize(100, 100)
        self.assertEqual(self.widget.get_size(), (100, 100))
        self.widget.resize(100, 20)
        self.assertEqual(self.widget.get_size(), (100, 20))


if __name__ == '__main__':
    unittest.main()
