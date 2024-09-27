from transformers import BertTokenizer, BertForMaskedLM
import torch

# Load the ProtBERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
model = BertForMaskedLM.from_pretrained("Rostlab/prot_bert")

