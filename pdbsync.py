from Bio import SwissProt
import requests
from Bio import PDB
from io import BytesIO, StringIO

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

# Function to load structure from a PDB URL
def load_structure_from_id(pdb_id):
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    response: requests.Response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    pdb_str = response.content.decode('utf-8')  # Decode bytes to string
    pdb_io = StringIO(pdb_str)  # Use StringIO to create a file-like object
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_id, pdb_io)
    return structure,parser

def process_pdb():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'PDB':
                    pdb_id = crossref[1]
                    print(f"Processing PDB ID: {pdb_id}")
                    structure,parser = load_structure_from_id(pdb_id)
                    print(f"Structure: {structure} Parser: {parser}")
                    for model in structure:
                        print(f"Model: {model}")
                        for chain in model:
                            print(f"Chain: {chain}")
                            for residue in chain:
                                print(f"Residue: {residue}")
                        
def process_pdb2():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'PDB':
                    pdb_id = crossref[1]
                    print(f"Processing PDB ID: {pdb_id}")
                    structure,parser = load_structure_from_id(pdb_id)
                    header = structure.header
                    compounds = header['compound']
                    for mol_id, compound_info in compounds.items():
                        print(f"MOL_ID: {mol_id}")
                        for key, value in compound_info.items():
                            print(f"  {key}: {value}")


process_pdb2()
