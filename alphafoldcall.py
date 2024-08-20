import os
import multiprocessing
import subprocess
import random
import time
from typing import Optional
import settings  # Assuming this is already defined in your environment
import data_manager  # Assuming this is already defined in your environment
import shutil



class StructureResult:
    def __init__(self, sequence, id=None, sequence_folder=None, structure_folder=None) -> None:
        # Initialize parameters
        self.sequence = sequence
        self.id = id if id else ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        self.sequence_folder = sequence_folder if sequence_folder else settings.sequences_folder
        self.structure_folder = os.path.join(structure_folder if structure_folder else settings.structure_folder, self.id)
        self.src_file = os.path.join(self.sequence_folder, f"{self.id}.fasta")
        self.stdout: str = None
        self.stderr: str = None
        self.process: multiprocessing.Process = None
        self.queue=multiprocessing.Queue()
        self.files=None
        self.is_amber=False
    def _write_fasta(self):
        
        fasta = f">{self.id}\n{self.sequence}\n"
        os.makedirs(self.sequence_folder, exist_ok=True)  # Ensure the sequence folder exists
        with open(self.src_file, 'w') as file:
            file.write(fasta)

    def generate_structure(self,amber:bool=False,templates:bool=False) -> 'StructureResult':
        self.is_amber=amber
        self._write_fasta()
        # Function to run the colabfold_batch script
        def run_colabfold(structure_result: 'StructureResult'):
            commands = ['./colabfold_batch', self.src_file, self.structure_folder]
            if templates:
                commands.append('--templates')
            if amber:
                commands.append('--amber')
            result = subprocess.run(commands,
                cwd=settings.alpha_fold_directory,
                capture_output=True,
                text=True
            )
            self.queue.put(result.stdout)
            self.queue.put(result.stderr)

        # Start the subprocess in a separate process
        self.process = multiprocessing.Process(target=run_colabfold, args=(self,))
        self.process.start()

        # Optionally return self to allow method chaining
        return self

    def join(self):
        """Wait for the subprocess to complete and retrieve stdout and stderr."""
        if self.process:
            #read from queue
            self.stdout=self.queue.get()
            self.stderr=self.queue.get()
        else:
            raise RuntimeError("No process has been started.")
    def list_structure(self):
        return os.listdir(self.structure_folder)
    
    def clear(self):
        if os.path.exists(self.src_file):
            os.remove(self.src_file)
        if os.path.exists(self.structure_folder):
            shutil.rmtree(self.structure_folder)
    def get_file(self,rank:int=1,relaxed:Optional[bool]=None)->Optional[str]:
        if relaxed is None:
            relaxed=self.is_amber
        if self.files is None:
            self.files=self.list_structure()
        #generate string from rank with at least 3 digits (e.g. 1 -> 001)
        rank_str = str(rank).zfill(3)
        relaxed_str = "relaxed" if relaxed else "unrelaxed"
        for i in self.files:
            if i.startswith(f"{self.id}_{relaxed_str}_rank_{rank_str}") and i.endswith(".pdb"):
                return i
        return None
    def get_absolute_file(self,rank:int=1,relaxed:Optional[bool]=None)->Optional[str]:
        file=self.get_file(rank,relaxed)
        if file is not None:
            return os.path.join(self.structure_folder,file)
        return None


if __name__ == "__main__":
    # Load samples
    samples = data_manager.load_samples("testsample")

    # Find the first sample without AlphaFold ID and no PDB ID
    sample = next((s for s in samples if len(s.alpha_fold_ids) == 0 and len(s.pdb_ids) == 0), None)

    result = StructureResult(sample.sequence, sample.id)

    result.generate_structure(True, True)
    result.join()
    import nglview as nv
    import ipywidgets
    #print list of files
    file=result.get_absolute_file()
        # Load the PDB file
    view = nv.show_file(file)

    # Display in a Jupyter notebook or standalone app
    view.display()
    

    


