import os
import unittest

import data_manager
import settings
from invoke import run
import subprocess
import alphafoldcall

class TestDataManager(unittest.TestCase):
   
   def test_load_samples(self):
      samples=data_manager.load_samples("testsample")
      print(f'sample length: {len(samples)}')
      self.assertIsNotNone(samples)
   
   def test_colab_fold(self):
      id='zuzkyqkekg'
      path=alphafoldcall.id_2_path(id)
      self.assertEqual(path,os.path.join(settings.structure_folder,id))
      for i in range(1,6):
         file=alphafoldcall.get_pdb(id,i,False)
         file_relaxed=alphafoldcall.get_pdb(id,i,True)
         print(f'relaxed: {file_relaxed} unrelaxed: {file}')
         self.assertIsNotNone(file)
         self.assertIsNotNone(file_relaxed)
      

      
        
    