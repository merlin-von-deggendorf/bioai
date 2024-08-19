import unittest

import data_manager

class TestDataManager(unittest.TestCase):
   
   def test_load_samples(self):
        samples=data_manager.load_samples("sample1")
        sample=samples[0]
        print(sample.sequence)
        self.assertTrue(True)
        
    