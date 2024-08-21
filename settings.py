
import json
import os
test_folder='/mnt/tests/'
base_folder = '/mnt/data/'
test_samples_folder=test_folder+'samples/'
test_structure_folder=test_folder+'structures/'
test_sequences_folder=test_folder+'sequences/'
folds_folder='/mnt/data/folds/'
alpha_fold_directory='/mnt/src/localfold/localcolabfold/colabfold-conda/bin/'
sequences_folder='/mnt/data/sequences/'
structure_folder='/mnt/data/structures/'
text_sample_folder='/mnt/data/text_samples/'
uni_prot_db = 'uniprot_sprot.dat'
abs_uni_prot_db = base_folder + uni_prot_db
samples_folder=base_folder+'samples/'
settings_path='~/.bioai/settings.json'
settings_file=None

class Settings:
    def __init__(self):
        self.swiss_line_count:int = 0

def save_settings() -> bool:
    global settings_file
    global settings_path
    if settings_file is not None:
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, 'w') as f:
            json.dump(settings_file.__dict__, f)
            return True
    return False

def load_settings() -> Settings:
    global settings_file
    global settings_path
    if settings_file is not None:
        return settings_file
    try:
        with open(settings_path, 'r') as f:
            settings_file = Settings()
            settings_file.__dict__ = json.load(f)
            return settings_file
    except:
        settings_file = Settings()
        return settings_file


#check if main
if __name__ == '__main__':
    import os
    # make sure all directories exist
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(test_samples_folder, exist_ok=True)
    os.makedirs(test_structure_folder, exist_ok=True)
    os.makedirs(test_sequences_folder, exist_ok=True)
    os.makedirs(folds_folder, exist_ok=True)
    os.makedirs(sequences_folder, exist_ok=True)
    os.makedirs(structure_folder, exist_ok=True)
    os.makedirs(text_sample_folder, exist_ok=True)
    os.makedirs(samples_folder, exist_ok=True)
