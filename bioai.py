import os
from typing import Optional
from Bio import SwissProt
import requests
import settings
import sys
import pickle

class Feature:
    def __init__(self):
        self.type=None
        self.location=None
        self.qualifiers={}
        pass
    def create_by_feature(self,feature:SwissProt.FeatureTable):
        self.type=feature.type
        self.location=feature.location
        for key in feature.qualifiers:
            self.qualifiers[key]=feature.qualifiers[key]
        pass
    def __str__(self):
        return f'{self.type} {self.location} {self.qualifiers}'
    def chebi_download(self,path:str) -> Optional[str]:
        chebiid:str=self.qualifiers.get('ligand_id')
        chebistart='ChEBI:CHEBI:'
        if chebiid.startswith(chebistart):
            chebiid=chebiid[len(chebistart):]
            print(f'Chebi id: {chebiid}')
            return download_chebi_molecule(chebiid,os.path.join(path,f'{chebiid}.mol'))
        else:
            return None


class Protein:
    def __init__(self):
        self.id=None
        self.sequence=None
        self.go_terms:list[int]=[]
        self.features:list[Feature]=[]
        self.alpha_folds=[]
        self.pdb_structures=[]
        pass
    def create_by_entry(self,record:SwissProt.Record):
        self.id = record.entry_name
        self.sequence = record.sequence
        for xref in record.cross_references:
            if xref[0] == 'GO':
                go_id = xref[1]
                if not go_id.startswith('GO:'):
                    sys.exit(f"Invalid GO ID: {go_id}")
                go_int = int(go_id[3:])
                self.go_terms.append(go_int)
            if xref[0]=='PDB':
                self.pdb_structures.append(str(xref[1]))
            if xref[0]=='AlphaFoldDB':
                self.alpha_folds.append(str(xref[1]))
            
        for feature in record.features:
            protein_feature = Feature()
            protein_feature.create_by_feature(feature)
            self.features.append(protein_feature)
    def __str__(self):
        string=f'{self.id}\n{self.sequence}\nGO terms:\n'
        for go in self.go_terms:
            string+=f'{go}\n'
        string+='Features:\n'
        for feature in self.features:
            string+=str(feature)+'\n'
        string+='PDB structures:\n'
        for pdb in self.pdb_structures:
            string+=pdb+'\n'
        string+='AlphaFold structures:\n'
        for af in self.alpha_folds:
            string+=af+'\n'
        return string
    def find_features_by_ligand(self,ligand:str) -> list[Feature]:
        features=[]
        for feature in self.features:
            if feature.qualifiers.get('ligand') == ligand:
                features.append(feature)
        return features
    def download_alpha_fold(self,directory:str) ->Optional[str]:
        for af in self.alpha_folds:
            return copy_alphafold_structure(af,directory)
        return None
    
        
class ProteinContainer:
    def __init__(self):
        self.proteins:list[Protein] = []
    def add_protein(self,protein:Protein):
        self.proteins.append(protein)
    def generate(self,skip=0,limit:int=None):
        with open(settings.abs_uni_prot_db, "r") as f:
            counter=0
            for i in range(skip):
                SwissProt.parse(f)

            for record in SwissProt.parse(f):
                protein = Protein()
                protein.create_by_entry(record)
                self.proteins.append(protein)
                if limit is not None:
                    counter+=1
                    if counter > limit:
                        break
    def find_by_id(self,id:str) -> Protein:
        for protein in self.proteins:
            if protein.id == id:
                return protein
        return None
    def get_ids(self) -> list[str]:
        return [protein.id for protein in self.proteins]
    def save(self,path:str=None):
        if path is None:
            path = settings.abs_protein_container
        with open(path, "wb") as f:
            pickle.dump(self,f)
    def load(path:str=None) -> 'ProteinContainer':
        if path is None:
            path = settings.abs_protein_container
        with open(path, "rb") as f:
            return pickle.load(f)
    def extract_ligands(self) -> dict[str:Feature]:
        ligands:dict[str:Feature] = {}
        ligand='ligand'
        ligandid='ligand_id'
        feature_type='BINDING'
        for protein in self.proteins:
            for feature in protein.features:
                if feature.type == feature_type and feature.qualifiers.get(ligandid) is not None:
                    ligand_id=feature.qualifiers[ligandid]
                    ligand_name=feature.qualifiers.get(ligand)
                    extracted=ligands.get(ligand_name)
                    if extracted is None:
                        extracted=ligands[ligand_name]=feature
                    if extracted.qualifiers.get(ligandid) != ligand_id:
                        print(f'Warning: Ligand {ligand_name} has multiple ids')
                    
        return ligands
    def find_by_ligand(self,ligand:str) -> list[str]:
        proteins=[]
        for protein in self.proteins:
            for feature in protein.features:
                if feature.qualifiers.get('ligand') == ligand:
                    proteins.append(protein.id)
                    break
        return proteins
    
def get_alphafold_structure(uniprot_id) -> Optional[str]:
    base_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.get(base_url)

    if response.status_code == 200:
        pdb_data = response.text
        return pdb_data
    else:
        return None
def copy_alphafold_structure(uniprot_id,path)->Optional[str]:
    base_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.get(base_url)

    if response.status_code == 200:
        storepath=os.path.join(path,f'{uniprot_id}.pdb')
        with open(storepath, "wb") as f:
            f.write(response.content)
            return storepath
    return None

def download_chebi_molecule(chebi_id, save_path):
    url = f'https://www.ebi.ac.uk/chebi/saveStructure.do?defaultImage=true&chebiId={chebi_id}&imageId=0'
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
            return save_path
    else:
        return None

def download_chebi_molecule2(chebi_id):
    url = f'https://www.ebi.ac.uk/chebi/saveStructure.do?sdf=true&chebiId={chebi_id}&imageId=0'
    response = requests.get(url)

    if response.status_code == 200:
        print(response.text)
    else:
        print(f'Failed to download {chebi_id}. HTTP status code: {response.status_code}')
