from transformers import BertTokenizer, BertForMaskedLM
import torch

# Set the device to GPU (CUDA)
device = torch.device("cuda")

# Load the ProtBERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
model = BertForMaskedLM.from_pretrained("Rostlab/prot_bert")

# Move the model to GPU
model = model.to(device)

# Example protein sequence to evaluate
sequence = "M E L K K L V I N"

# Tokenize the sequence (ProtBERT requires space-separated amino acids)
inputs = tokenizer(sequence, return_tensors="pt")

print(inputs)

sequence = "MELKKLVIN"

# Tokenize the sequence (ProtBERT requires space-separated amino acids)
inputs = tokenizer(sequence, return_tensors="pt")

print(inputs)