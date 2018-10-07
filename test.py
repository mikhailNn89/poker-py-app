import unittest
import sys

class Test1(unittest.TestCase):
    def setUp(self):
        print('Test #1 begin')
    
    def test1(self):
        print('Inside test #1')
        self.assertEqual(20,20)
        
    def tearDown(self):
        print('Test #1 end')    
        
if __name__ == '__main__':
    unittest.main()        
