import csv
import itertools
import sys
import math

# Dictionary {}
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


#  Test printing PROBS

def main():
    # # Check for proper usage
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python heredity.py data.csv")
    # people = load_data(sys.argv[1])
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

    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )

        # print(have_trait, fails_evidence)
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                print(one_gene,",", two_genes,",", have_trait,",", p)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    # normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


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


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    def check_trait(person, genes):

        if person in have_trait:
            return PROBS["trait"][genes][True]
        else:
            return PROBS["trait"][genes][False]

    def check_parents(person, genes):

        # initialize variables
        mom = people[person]["mother"]
        dad = people[person]["father"]

        # return p_parent_gene if no parents (UNCONDITIONAL)
        if mom is None and dad is None:
            return PROBS["gene"][genes]

        # joint probabilities for mom, dad (in that order)
        p_parents = []

        # Find mutation probability for <0,1,2> genes
        for parent in [mom, dad]:
            p_parent_gene = 0

            if parent in two_genes:  # if parent has 2 genes, 99% mutation
                p_parents.append(1 - PROBS["mutation"])
            elif parent in one_gene:  # if parent has 1 gene, 50% mutation
                p_parents.append(0.5)
            else:  # if parent has 0 gene, 1% mutation
                p_parents.append(PROBS["mutation"])

        # probability inheriting 2 genes
        if genes == 2:
            return (p_parents[0] * p_parents[1])

        # probability inheriting 1 gene
        elif genes == 1:
            return ((1 - p_parents[0]) * (p_parents[1])) + \
                   ((p_parents[0]) * (1 - p_parents[1]))

        # probability inheriting 0 gene
        else:
            return ((1 - p_parents[0]) * (1 - p_parents[1]))

    # Initialize variable
    p_joint = []

    for person in people:

        p_gene = 0
        p_trait = 0

        if person in two_genes:
            p_gene = check_parents(person, 2)
            p_trait = check_trait(person, 2)
        elif person in one_gene:
            p_gene = check_parents(person, 1)
            p_trait = check_trait(person, 1)
        else:
            p_gene = check_parents(person, 0)
            p_trait = check_trait(person, 0)

        p_joint.append(p_gene * p_trait)

    return math.prod(p_joint)
    # print(list(people.keys()), one_gene, two_genes, have_trait)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        # initialize variables
        genes = 0
        trait = False

        # Determine if person has <0, 1, 2> genes
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2

        # Determine if person has trait or not
        if person in have_trait:
            trait = True

        # update joint probabilities
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene
        gene_2 = probabilities[person]["gene"][2]
        gene_1 = probabilities[person]["gene"][1]
        gene_0 = probabilities[person]["gene"][0]

        gene_normalizer = 1 / (gene_0 + gene_1 + gene_2)

        # Update genes
        probabilities[person]["gene"][2] = gene_2 * gene_normalizer
        probabilities[person]["gene"][1] = gene_1 * gene_normalizer
        probabilities[person]["gene"][0] = gene_0 * gene_normalizer

        # Normalize trait
        true_trait = probabilities[person]["trait"][True]
        false_trait = probabilities[person]["trait"][False]

        trait_normalizer = 1 / (true_trait + false_trait)

        # Update traits
        probabilities[person]["trait"][True] = true_trait * trait_normalizer
        probabilities[person]["trait"][False] = false_trait * trait_normalizer


if __name__ == "__main__":
    main()
