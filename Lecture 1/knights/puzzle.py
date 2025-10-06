from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # All persons can either be a knight or a knave, not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # If A is a knight, A is telling the truth
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, A is telling the opposite of the truth
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # All persons can either be a knight or a knave, not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # A is a knight only if the statement is true
    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # All persons can either be a knight or a knave, not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # A is a knight only if the statement is true
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # B is a knight only if the statement is true
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # All persons can either be a knight or a knave, not both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # We don't know what A stated

    # If B is a knight, B is telling the truth
    # This implication isn't very obvious, but necessary.  Basically, A HAS to be a knight. If B is a knight, then this statement exposes the contradiction.
    Implication(BKnight, AKnight),
    # B is a knight only if the statement is true
    Biconditional(BKnight, CKnave),

    # C is a knight only if the statement is true
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
