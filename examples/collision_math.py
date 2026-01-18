#!/usr/bin/env python3
"""
Understanding Collision Probability in Stochastic Pseudonymizer

This script demonstrates the math behind token collision rates.
Run it to see how different token lengths and population sizes
affect plausible deniability.

The core insight: shorter tokens = more collisions = stronger deniability
but noisier analytics. Longer tokens = fewer collisions = weaker deniability
but cleaner analytics.
"""

import math


def collision_probability(population: int, hex_chars: int) -> float:
    """
    Calculate the probability that any given patron shares their token
    with at least one other patron in the population.

    Based on the birthday problem. For a population of n patrons and
    m possible tokens:

        P(collision) ≈ 1 - e^(-n/m)

    For small probabilities, this simplifies to approximately n/m.

    Args:
        population: Number of patrons (current or lifetime estimate)
        hex_chars: Number of hex characters in the token (determines m = 16^hex_chars)

    Returns:
        Probability as a float between 0 and 1
    """
    possible_tokens = 16**hex_chars
    return 1 - math.exp(-population / possible_tokens)


def format_as_one_in_x(probability: float) -> str:
    """
    Convert a probability to human-readable '1 in X' format.

    This is more intuitive for legal/privacy discussions than percentages.
    '1 in 48' is easier to grasp than '2.08%'.
    """
    if probability == 0:
        return "never"
    x = round(1 / probability)
    return f"1 in {x:,}"


def print_collision_table():
    """Print the collision rate table used in the README."""
    print("Collision rates by population and token length")
    print("=" * 70)
    print("(Read as: probability that any given patron shares their token)\n")

    populations = [10_000, 50_000, 100_000, 350_000, 500_000, 1_000_000, 2_000_000]
    hex_lengths = [5, 6, 7]

    # Header
    header = "Population".ljust(15) + "".join(
        [f"{h} chars".center(15) for h in hex_lengths]
    )
    print(header)
    print("-" * 60)

    for pop in populations:
        row = f"{pop:,}".ljust(15)
        for hex_c in hex_lengths:
            prob = collision_probability(pop, hex_c)
            row += format_as_one_in_x(prob).center(15)
        print(row)


def analyze_your_library(current_patrons: int, lifetime_estimate: int):
    """
    Analyze collision rates for a specific library.

    Args:
        current_patrons: Current active patron count
        lifetime_estimate: Estimated total patron IDs over system lifetime
    """
    print(f"\nAnalysis for your library")
    print(f"Current patrons: {current_patrons:,}")
    print(f"Lifetime estimate: {lifetime_estimate:,}")
    print("=" * 50)

    for hex_c in [5, 6, 7]:
        prob_now = collision_probability(current_patrons, hex_c)
        prob_lifetime = collision_probability(lifetime_estimate, hex_c)
        print(f"\n{hex_c} hex characters:")
        print(f"  Now:      {format_as_one_in_x(prob_now)}")
        print(f"  Lifetime: {format_as_one_in_x(prob_lifetime)}")


def explain_the_math():
    """Explain the underlying math."""
    print("\nHow the math works")
    print("=" * 50)
    print(
        """
Each hex character represents 4 bits, giving 16 possible values (0-9, a-f).
So the number of possible tokens for a given length is:

  5 chars = 16^5 = 1,048,576       (~1 million)
  6 chars = 16^6 = 16,777,216      (~17 million)
  7 chars = 16^7 = 268,435,456     (~268 million)

The collision probability for any individual patron is approximately:

  P(collision) ≈ population / possible_tokens

This comes from the birthday problem in probability theory.

Example: 350,000 patrons with 6-character tokens
  P = 350,000 / 16,777,216 = 0.0209 = 2.09%
  Or: 1 in 48 patrons share their token with someone else.
"""
    )


if __name__ == "__main__":
    print_collision_table()
    print()
    explain_the_math()

    # Example: analyze a specific library
    # Uncomment and modify for your own analysis:
    # analyze_your_library(current_patrons=350_000, lifetime_estimate=1_000_000)
