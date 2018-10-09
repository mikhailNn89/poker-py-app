import unittest
import sys

def assertTest():
    print('Test #0 beginning')
    self.assertEqual(20,20)

class Test1(unittest.TestCase):
    def setUp(self):
        print('Test #1 before')
    
    def test1(self):
        print('Test #1 beginning')
        self.assertEqual(20,20)
        
    def tearDown(self):
        print('Test #1 end')    
        
if __name__ == '__main__':
    unittest.main()        
