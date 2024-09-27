import tkinter as tk
import sample_manager as sm
import bert_validation as bv
import alphafoldcall

class AutoCombiner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoCombiner")
        self.button = tk.Button(self.root, text="Combine", command=self.combine)
        self.button.grid(row=2,column=0,columnspan=2)

        self.original_sequence =SequenceGUI(self.root,0,0)
        self.original_sequence.set_sequence('ATGAGTATATTTGACGAGCTCCGTGCGGTAAACGTAAATAACCACACGGAAGAAAAGAACGGACTTAAATATCTTTCCTGGGCGTGGGCTTGGGATGAGGTTATGCAGAGATATCCGGGGGCTGTGTATGAGATCAAAGAGTTTGACGGTAAGCCATACCTTTATGATGACAAGCTGGGATATCTTGTTATGACAACAATGACGATAGACGGCATCACGCGGACGATGTGGCTTCCAGTTATGGACGGGGCGAACAAAGCCATGAAGGATGCCCCGTATGAATATCAGGTAAAAGAATATGTCAATCGGAAATGGACTGGGAAATATGTAGACAAGACGGTAGAGGCAGCAACGATGTTTGATATCAATACAGCGATTATGCGCTGTCTGGTTAAAAATATCGCTATGTTTGGCTTGGGATTGTATATCTATTCTGGCGAGGATCTTCCGCCGGAACAACCAAAAAAATTGACAAAAGCACAGGTTACAACGCTAGAGGAATGCATTCCGAAGCACGGTCAGACGATCGAAAAGGTTTGCGACTCATTTAAGGTCAAGAATCTTTCTGATCTTACGGTTGACCAGTTTATGTGGCTCATGGATCGGATGGGAGAAAAATGA')
        self.added_sequence = SequenceGUI(self.root,1,0)
        self.added_sequence.set_sequence('PPKKKRKV')
        self.result=SequenceGUI(self.root,3,0)
        self.result.set_sequence('')
        self.sample_manger=sm.SampleManager(self.root)
        self.result_text = tk.Text(self.root,width=50,height=10)
        self.result_text.grid(row=4,column=0)

        self.root.mainloop()
        
    
    def combine(self):
        original_sequence=self.original_sequence.get()
        inserted_sequence=self.added_sequence.get()
        print(f"Original: {original_sequence}")
        print(f"Inserted: {inserted_sequence}")
        combiner = bv.Combiner(original_sequence,inserted_sequence)
        result,start,end = combiner.combine()
        self.result.set_sequence(result)
        self.result_text.delete("1.0",tk.END)
        self.result_text.insert(tk.END,f"Start: {start}\nEnd: {end}\n{result}")

class SequenceGUI:
    def __init__(self,frame,row,column):
        self.subframe = tk.Frame(frame)
        self.subframe.grid(row=row,column=column)
        self.side_bar = tk.Frame(self.subframe)
        self.side_bar.grid(row=0,column=0)
        self.label = tk.Label(self.side_bar,text="Sequence")
        self.label.grid(row=0,column=0)
        self.load_button = tk.Button(self.side_bar,text="Fold",command=self.fold)
        self.load_button.grid(row=1,column=0)
        self.sequence = tk.Text(self.subframe,width=50,height=10)
        self.sequence.config(wrap=tk.NONE)
        self.sequence.grid(row=0,column=1)
        self.copy_button = tk.Button(self.side_bar,text="Copy",command=self.copy)
        self.copy_button.grid(row=2,column=0)
        self.insert_button = tk.Button(self.side_bar,text="Insert",command=self.insert)
        self.insert_button.grid(row=3,column=0)
    def copy(self):
        self.sequence.clipboard_clear()
        self.sequence.clipboard_append(self.get())
        self.sequence.update()
    def insert(self):
        # clear text
        self.sequence.delete("1.0",tk.END)
        # insert text from global clipboard
        self.sequence.insert(tk.INSERT,self.sequence.clipboard_get())

    def set_sequence(self,sequence:str):
        self.sequence.delete("1.0",tk.END)
        self.sequence.insert(tk.END,sequence)
    def get(self):
        sequence= self.sequence.get("1.0",tk.END)
        # remove all whitespace and newlines
        sequence = ''.join(sequence.split())
        return sequence
        
    def fold(self):
        print(f"Fold: {self.get()}")
        sequence=self.get()
        print(sequence)
        structure_result=alphafoldcall.StructureResult(sequence)
        structure_result.generate_structure(amber=True)
        structure_result.join()
        self.structure_result=structure_result
        print(structure_result.stdout)
        print(structure_result.stderr)
        



if __name__ == "__main__":
    AutoCombiner()