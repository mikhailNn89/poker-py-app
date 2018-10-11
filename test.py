import unittest
import pytest
import sys
from t_class import *

# Arseny: did you run this? What is 'self'? What for is this function?
def test_myTest():
    print('Test #0')
    self.assertEqual(20,20)

class Test1(unittest.TestCase):
    def setUp(self):
        print('Test before')
    
    def test1(self):
        print('Test #1')
        self.assertEqual(20,20)
        
    def test2(self):
        print('Test #2')
        obj = TestedClass()
        self.assertEqual(obj.foo(),7)    
        
    def tearDown(self):
        print('Test end')    
        
if __name__ == '__main__':
    unittest.main()        
