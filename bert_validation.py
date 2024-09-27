from transformers import BertTokenizer, BertForMaskedLM
import torch

# Set the device to GPU (CUDA)
device = torch.device("cuda")

# Load the ProtBERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
model = BertForMaskedLM.from_pretrained("Rostlab/prot_bert")

# Move the model to GPU
model = model.to(device)
model.eval()



def calculate_log_likelihood(sequence):# Move inputs to GPU
    # add space between each character of the sequence
    sequence = ' '.join(sequence)
    # Tokenize the sequence (ProtBERT requires space-separated amino acids)
    inputs = tokenizer(sequence, return_tensors="pt")
    # Move inputs to GPU
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Forward pass through the model
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Move logits back to CPU for further processing
    logits = logits.cpu()

    # Calculate log-likelihood score for the sequence
    probabilities = torch.softmax(logits, dim=-1)
    max_probs = probabilities.max(dim=-1).values
    log_likelihood = max_probs.log().mean().item()

    return log_likelihood
class Combiner:
    def __init__(self,original_sequence,inserted_sequence):
        self.original_sequence = original_sequence
        self.inserted_sequence = inserted_sequence
        
    def combine(self) -> tuple[str,int,int]:
        len_inserted_sequence = len(self.inserted_sequence)
        self.max_offset = len(self.original_sequence)-len_inserted_sequence
        best_score = -float('inf')
        best_offset = -1
        for i in range(self.max_offset+1):
            combined_sequence = self.combine_strings(i)
            log_likelihood = calculate_log_likelihood(combined_sequence)
            if log_likelihood > best_score:
                best_score = log_likelihood
                best_offset = i
        self.best_offset = best_offset
        return self.combine_strings(best_offset),best_offset,best_offset+len_inserted_sequence
    def combine_strings(self,offset)->str:
        return self.original_sequence[:offset]+self.inserted_sequence+self.original_sequence[offset+len(self.inserted_sequence):]
        
if __name__ == "__main__":
    sequence ='MFVDQVKVYVKGGDGGNGAVSFRREKYVPLGGPAGGDGGQGGDVVFVVDEGLRTLVDFRYQRHFKAPRGEHGRNKSQHGAGAEDMVVRVPPGTTVIDDDTKEVIADLVEQGQRAVIAKGGRGGRGNNRFANSSNPAPHISENGEPGQERYIVMELKLIADVGLVGYPSVGKSTLLSSVTAAKPKIAAYHFTTLTPNLGVVDLGERSFVMADLPGLIEGAHEGVGLGHQFLRHVERTRLIVHVIDMAAVDGRDPYEDYLQINRELTLYNLKLEDRPQIVVANKMELPEAEENLRIFKEKAPDVKVYEISAATSKGVQELMYAIGDTLATIPDKPAVEEVAEVEERVVFRAEKEPDAFEITRDNEVFVVSGEKIEKLVRMTNLNSYDAAQRFARQMRSMGVDDALRKLGAKDGDTVRIGKLEFDFVE'
    inserted_sequence = 'DCPGH'
    # sequence='DCPGHG'
    # inserted_sequence='ABC'
    combiner=Combiner(sequence,inserted_sequence)
    solution=combiner.combine()
    print(solution)