import cobra
from cobra.io import load_model
# "iJO1366" and "salmonella" are also valid arguments
model = load_model("iJO1366")

print(len(model.reactions))
print(len(model.metabolites))
print(len(model.genes))

print(model.name)