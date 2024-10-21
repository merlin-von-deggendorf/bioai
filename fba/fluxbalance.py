import cobra
from cobra import Model, Reaction, Metabolite

# Initialize the model
model = Model("simple_model")

# Create metabolites (A, B, C)
A = Metabolite("A", compartment="c")
B = Metabolite("B", compartment="c")
C = Metabolite("C", compartment="c")

# Create reactions
# Reaction 1: A -> B
reaction1 = Reaction("R1")
reaction1.name = "A to B"
reaction1.lower_bound = 0  # irreversible reaction
reaction1.upper_bound = 1000
reaction1.add_metabolites({A: -1, B: 1})

# Reaction 2: B -> C
reaction2 = Reaction("R2")
reaction2.name = "B to C"
reaction2.lower_bound = 0  # irreversible reaction
reaction2.upper_bound = 1000
reaction2.add_metabolites({B: -1, C: 1})

# Biomass reaction (maximize this in FBA)
# Reaction 3: C -> Biomass
reaction3 = Reaction("Biomass")
reaction3.name = "C to Biomass"
reaction3.lower_bound = 0
reaction3.upper_bound = 1000
reaction3.add_metabolites({C: -1})

# Add an exchange reaction for A (source of A)
exchange_A = Reaction("EX_A")
exchange_A.name = "Exchange A"
exchange_A.lower_bound = -1000  # allows inflow of A
exchange_A.upper_bound = 0
exchange_A.add_metabolites({A: 1})

# Add reactions to the model
model.add_reactions([reaction1, reaction2, reaction3, exchange_A])

# Set the objective to maximize the Biomass reaction
model.objective = "Biomass"

# Perform FBA
solution = model.optimize()

# Check if the solution is optimal
if solution.status == 'optimal':
    print(f"Objective value (Biomass production): {solution.objective_value}")
    print("Fluxes through reactions:")
    for reaction in model.reactions:
        print(f"{reaction.id}: {solution.fluxes[reaction.id]}")
else:
    print(f"Solution status: {solution.status}")
    print("No feasible solution found.")

# Print solver summary to investigate potential issues
print("\nSolver summary:")
model.summary()
