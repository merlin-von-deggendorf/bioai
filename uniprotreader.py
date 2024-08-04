from Bio import SeqIO

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

# Get the full file path
file_path = get_uni_prot_file()

ids = []
# Parse the UniProtKB flat file
with open(file_path, 'r') as file:
    cntr=0
    for record in SeqIO.parse(file, 'swiss'):
        ids.append(record.id)

print('Total number of records:', len(ids))

