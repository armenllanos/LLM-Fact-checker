import unittest

class test_String(unittest.TestCase):
    def test_empty(self):
        self.assertEquals("","")
        
if __name__ == '__main__':
    unittest.main()