import unittest

import data_manager

class TestDataManager(unittest.TestCase):
    def load_samples(self):
        samples=data_manager.load_samples("sample1")
        print(len(samples))
        self.assertTrue(True)


    