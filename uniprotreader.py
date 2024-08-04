from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio import SwissProt

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

def read_annotations():
    # Get the full file path
    file_path = get_uni_prot_file()
    # Parse the UniProtKB flat file using SwissProt
    cntr=0
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs: list[str] = record.cross_references
            for crossref in crossrefs:
                print(crossref)
            cntr+=1
            if cntr>1000:
                break   
        
            
def extract_sample(end_line):
    file_path = get_uni_prot_file()
    output_file = base_folder + 'sample.dat'
    # write all the lines until end_line and write them to output_file
    with open(file_path, 'r') as file:
        with open(output_file, 'w') as out:
            for i in range(end_line):
                line = file.readline()
                out.write(line)
                
            

read_annotations()


