from constraint import *

problem = Problem()

# Add variables
# problem.addVariables(
#     ["A", "B", "C", "D", "E", "F", "G"],
#     ["Monday", "Tuesday", "Wednesday"]
# )

problem.addVariables(
    ["A", "C", "D", "E", "G"],
    ["Monday", "Tuesday", "Wednesday"]
)

problem.addVariables(
    ["B"],
    ["Tuesday"]
)

problem.addVariables(
    ["F"],
    ["Wednesday"]
)

# Add constraints
CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("F", "G")
]
for x, y in CONSTRAINTS:
    problem.addConstraint(lambda x, y: x != y, (x, y))

# Solve problem
for solution in problem.getSolutions():
    print(solution)
