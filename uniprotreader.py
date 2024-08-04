from Bio import SeqIO

# Define the base folder and UniProtKB file name
base_folder = '/mnt/data/'
uni_prot_db = 'uniprot_sprot.dat'

# Function to get the full file path
def get_uni_prot_file():
    return base_folder + uni_prot_db

# Get the full file path
file_path = get_uni_prot_file()

# Parse the UniProtKB flat file
with open(file_path, 'r') as file:
    cntr=0
    for record in SeqIO.parse(file, 'swiss'):
        # Print the record ID
        print(f"ID: {record.id}")
        
        # Print the record description
        print(f"Description: {record.description}")
        
        # Print the sequence
        print(f"Sequence: {record.seq}")
        
        # Access annotations
        for key, value in record.annotations.items():
            print(f"{key}: {value}")
        
        # Access features
        for feature in record.features:
            print(f"Feature: {feature.type}")
            print(f"Location: {feature.location}")
            print(f"Qualifiers: {feature.qualifiers}")
        
        print("-" * 40)

        # Break after 5 records
        cntr += 1
        if cntr == 5:
            break
