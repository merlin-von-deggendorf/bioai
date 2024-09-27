from transformers import EsmTokenizer, EsmForSequenceClassification
import torch

# Set device to GPU (CUDA) directly
device = torch.device("cuda")

# Load the ESM-2 model and tokenizer
tokenizer = EsmTokenizer.from_pretrained("facebook/esm2_t33_650M_UR50D")
model = EsmForSequenceClassification.from_pretrained("facebook/esm2_t33_650M_UR50D")

# Move the model to GPU (CUDA)
model = model.to(device)

# Example protein sequence
sequence = "MELKKLVINTHA"

# Tokenize the sequence
inputs = tokenizer(sequence, return_tensors="pt")

# Move the inputs to GPU (CUDA)
inputs = {key: value.to(device) for key, value in inputs.items()}

# Evaluate the sequence
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

# Move the logits back to CPU for further processing
logits = logits.cpu()

# Calculate the validity score
validity_score = torch.sigmoid(logits).item()
print(f"Validity score: {validity_score}")
