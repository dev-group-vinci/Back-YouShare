import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
