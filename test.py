import unittest

print('Blank test')

class TestBlank(unittest.TestCase):
    def test1(self):
        print('Blank test 1')
        self.assertEqual(20,20)
        
if __name__ == '__main__':
    unittest.main()        
