import os
import unittest

import data_manager
import settings
from invoke import run
import subprocess


class TestDataManager(unittest.TestCase):
   
   def test_load_samples(self):
      samples=data_manager.load_samples("testsample")
      print(f'sample length: {len(samples)}')
      self.assertIsNotNone(samples)
   
   def test_colab_fold(self):
      import alphafoldcall


      
        
    