import os
import unittest

import data_manager
import settings



class TestDataManager(unittest.TestCase):
   
   def test_load_samples(self):
      samples=data_manager.load_samples("testsample")
      print(f'sample length: {len(samples)}')
      self.assertIsNotNone(samples)
   
   def test_colab_fold(self):
      samples=data_manager.load_samples("testsample")
      #find sample without alpha fold id and no pdb id
      sample=None
      for s in samples:
         if len(s.alpha_fold_ids)==0 and len(s.pdb_ids)==0:
            sample=s
            break
      self.assertIsNotNone(sample)
      #copy fasta to test folder
      #make sure structure folder exists
      if not os.path.exists(settings.test_structure_folder):
         os.makedirs(settings.test_structure_folder)
      #make sure sequences folder exists
      if not os.path.exists(settings.test_sequences_folder):
         os.makedirs(settings.test_sequences_folder)
      
      fasta=sample.create_fasta()
      #save fasta to sequences folder
      with open(settings.test_sequences_folder+sample.id+".fasta",'w') as file:
         file.write(fasta)
      
      #run alphafold
      
      
        
    