UNIPROT_FILE='/mnt/ramdisk/uniprot_sprot.dat'


if __name__ == '__main__':
    import os
    # make sure the file UNIPROT_FILE exists
    if not os.path.exists(UNIPROT_FILE):
        raise FileNotFoundError(f"UNIPROT_FILE {UNIPROT_FILE} not found")