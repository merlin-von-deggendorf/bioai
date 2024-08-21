from Bio import SwissProt
import requests
from Bio import PDB
from io import BytesIO, StringIO
import sys
import data_manager
import settings


def analyze_go_terms():
    # Get the full file path
    goterms: dict[int, int] = {}
    file_path = settings.abs_uni_prot_db
    # Parse the UniProtKB flat file using SwissProt
    with open(file_path, 'r') as file:
        for record in SwissProt.parse(file):
            crossrefs = record.cross_references
            for crossref in crossrefs:
                if crossref[0] == 'GO':
                    go_id = crossref[1]
                    if not go_id.startswith('GO:'):
                        sys.exit(f"Invalid GO ID: {go_id}")
                    go_int = int(go_id[3:])
                    goterm=goterms.get(go_int,0)
                    goterms[go_int]=goterm+1
                    

if __name__ == '__main__':
    analyze_go_terms()
                    
                        

