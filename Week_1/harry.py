from logic import *

# rain = Symbol("rain")
# hagrid = Symbol("hagrid")
# dumbledore = Symbol("dumbledore")
#
# knowledge = And(
#     Implication(Not(rain), hagrid),
#     Or(hagrid, dumbledore),
#     Not(And(hagrid, dumbledore)),
#     dumbledore
# )
#
# print(model_check(knowledge, rain))

P = Symbol("P")
Q = Symbol("Q")
R = Symbol("R")
S = Symbol("S")

kb = And(
    Implication(Q, P),
    P,
    And(R, Not(R)),
    Not(R),
    Or(P, R),
    Or(Not(P), Q),
    Or(R, Q)
)

# print(model_check(Implication(Q, P), P))
# print(model_check(Or(Not(Q), P), P))
# print(model_check(P, Implication(Q, P)))
print(model_check(And(R, Not(R)), Not(R)))
# print(model_check(And(Or(P, R), Or(Not(P), Q)), Or(R, Q)))