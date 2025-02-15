import csv
import itertools
import sys
import pandas as pd
import numpy as np


# for letter in 'Python':     # First Example
#    if letter == 'h':
#       continue
#    print('Current Letter :', letter)


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

# print(PROBS["gene"])
# print(PROBS["gene"][0])
# print(PROBS["gene"][1])
# print(PROBS["gene"][2])
#
# print(PROBS["trait"])
# print(PROBS["trait"][0][True])
# print(PROBS["trait"][0][False])
#
# print(PROBS["trait"][1][True])
# print(PROBS["trait"][1][False])
#
# print(PROBS["trait"][2][True])
# print(PROBS["trait"][2][False])

def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


people = load_data("data/family0.csv")

# Keep track of gene and trait probabilities for each person
probabilities = {
    person: {
        "gene": {
            2: 0,
            1: 0,
            0: 0
        },
        "trait": {
            True: 0,
            False: 0
        }
    }
    for person in people
}

# print(probabilities)

# print(probabilities['Lily'])
print(probabilities['Lily']['gene'])
# print(probabilities['Lily']['trait'])

# print(probabilities[people["Harry"]["mother"]])
# print(people["Harry"]["mother"])

# for person in people:
#     mom = people[person]["mother"]
#     dad = people[person]["father"]
#
#     parents = [mom, dad]
#     print(parents)

count = 0
for genes in probabilities["Lily"]["gene"]:
    probabilities["Lily"]["gene"][genes] = genes + count
    count += 1

print(probabilities["Lily"]["gene"])