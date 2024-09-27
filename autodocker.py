import settings
import os
import shutil
import bioai

# Your code here

class AutoDocker:
    def __init__(self,protein:bioai.Protein,feature:bioai.Feature) -> None:
        print(f"AutoDocker: {protein.id} {feature}")
        self.clear_autodock_working_directory()
        self.protein = protein
        alpha_fold = protein.download_alpha_fold(settings.autodock_working_directory)
        mol=feature.chebi_download(settings.autodock_working_directory)
        print(f'AlphaFold: {alpha_fold} Ligand: {mol}')
        #convert to pdbqt using obabel
        self.alpha_pdbqt=self.convert_to_pdbqt(alpha_fold)
        self.ligand_pdbqt=self.convert_to_pdbqt(mol)
    def convert_to_pdbqt(self, file_path:str):
        #find index of last dot
        last_dot_index = file_path.rfind('.')
        #replace last dot with .pdbqt
        pdbqt_file = file_path[:last_dot_index]+'.pdbqt'
        os.system(f'obabel {file_path} -O {pdbqt_file} --partialcharge gasteiger')
        return pdbqt_file
        

    def clear_autodock_working_directory(self):
        if os.path.exists(settings.autodock_working_directory):
            shutil.rmtree(settings.autodock_working_directory)
        os.makedirs(settings.autodock_working_directory)

if __name__ == '__main__':
    protein_container = bioai.ProteinContainer.load(settings.samples_folder+'reduced')
    #get randorm protein with binding feature
    import random
    from tkinter import Tk, messagebox
    def find_random_protein(protein_container:bioai.ProteinContainer) -> tuple[bioai.Protein,bioai.Feature]:
        while True:
            protein = random.choice(protein_container.proteins)
            if len(protein.alpha_folds) > 0:
                for feature in protein.features:
                    if feature.type == 'BINDING':
                        ligand_id = feature.qualifiers.get('ligand_id')
                        ligand_name = feature.qualifiers.get('ligand')
                        if ligand_id is not None:
                            
                            root = Tk()
                            root.withdraw()

                            user_input = messagebox.askquestion("User Input", f"Accept: {ligand_name}")

                            if user_input == 'yes':
                                return protein, feature
    protein,feature = find_random_protein(protein_container)
    autodocker=AutoDocker(protein,feature)

            