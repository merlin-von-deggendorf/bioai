from Bio import SwissProt
from Bio.SwissProt import Record
import random
import json
import pickle

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'
samples_path=base_folder+'samples/'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

def extract_sample(sample_size:int):
    samples : list['Sample']=[]
    with open(get_uni_prot_file(), 'r') as file:
        records:list[Record]=[]
        for record in SwissProt.parse(file):
            records.append(record)
        #extract random sample
        for i in range(sample_size):
            random_record=random.choice(records)
            sample=Sample(random_record)
            samples.append(sample)

    return samples

def write_samples(samples:list['Sample'],file_name):
    path=samples_path+file_name
    with open(path,'wb') as file:
        #write samples as json
        pickle.dump(samples,file)
def load_samples(name:str) -> list['Sample']:
    with open(samples_path+name,'rb') as file:
        samples=pickle.load(file)
    return samples
def create_sample_file(sample_size:int,file_name:str):
    samples=extract_sample(sample_size)
    write_samples(samples,file_name)

class Sample:
    def __init__(self,record:Record):
        self.id=str(record.entry_name)
        self.sequence=str(record.sequence)
        #extract alpha fold ids
        #extract pdb ids
        self.pdb_ids=[]
        self.alpha_fold_ids=[]
        for xref in record.cross_references:
            if xref[0]=='PDB':
                self.pdb_ids.append(str(xref[1]))
            if xref[0]=='AlphaFoldDB':
                self.alpha_fold_ids.append(str(xref[1]))
    def create_fasta(self):
        return '>'+self.id+'\n'+self.sequence+'\n'

class SampleList:
    def __init__(self,samples:list[Sample]):
        self.samples=samples
    def get_sample_by_id(self,id:str):
        for sample in self.samples:
            if sample.id==id:
                return sample
        return None