
from Bio import SwissProt
import requests
from Bio import PDB
from Bio.PDB import PDBParser, Structure
from io import BytesIO

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

def get_alphafold_structure(uniprot_id):
    base_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.get(base_url)

    if response.status_code == 200:
        pdb_data = response.text
        return pdb_data
    else:
        return None


def read_annotations():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    cntr=0
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs: list[str] = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'AlphaFoldDB':
                    pdb_data = get_alphafold_structure(crossref[1])
                    if pdb_data is None:
                        print(f"Could not fetch the structure for {crossref[1]}")
                    break

            # cntr+=1
            # if cntr>1000:
            #     break   


def download_pdb(pdb_id):
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response = requests.get(url)
    # store the pdb file to a string
    pdb_data = response.text
    return pdb_data

def find_pdb():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    cntr=0
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs: list[str] = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'PDB':
                    pdb_string=download_pdb(crossref[1])
                    #tore pdb string to a file in the data directory
                    with open(f'/mnt/data/pdbs/{crossref[1]}.pdb', 'w') as file:
                        file.write(pdb_string)
                    break
            
def extract_sample(end_line):
    file_path = get_uni_prot_file()
    output_file = base_folder + uni_prot_db
    # write all the lines until end_line and write them to output_file
    with open(file_path, 'r') as file:
        with open(output_file, 'w') as out:
            for i in range(end_line):
                line = file.readline()
                out.write(line)
                
            
# Function to load structure from a PDB URL
def load_structure_from_id(id):
    url = f'https://files.rcsb.org/download/{id}.pdb'
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    pdb_io = BytesIO(response.content)
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('protein', pdb_io)
    return structure

def process_pdb():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    cntr=0
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs: list[str] = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'PDB':
                    structure=load_structure_from_id(crossref[1])

                    break

if __name__ == '__main__':
    process_pdb()