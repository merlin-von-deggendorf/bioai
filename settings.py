test_folder='/mnt/tests/'
test_samples_folder=test_folder+'samples/'
test_structure_folder=test_folder+'structures/'
test_sequences_folder=test_folder+'sequences/'
folds_folder='/mnt/data/folds/'
alpha_fold_directory='/mnt/src/localfold/localcolabfold/colabfold-conda/bin/'
sequences_folder='/mnt/data/sequences/'
structure_folder='/mnt/data/structures/'


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
    