# Stochastic Pseudonymizer

Generate pseudonymous tokens from patron IDs with **built-in plausible deniability**.

## What This Does

Given a patron ID and a secret key, this library produces a short token (like `a7f2b3`) that:

1. **Is deterministic** — the same patron ID always produces the same token
2. **Cannot be reversed** — you can't derive the patron ID from the token without the secret
3. **Has intentional collisions** — multiple patron IDs may produce the same token

That third property is the key feature. It means that even if someone has your secret key and algorithm, they cannot prove with certainty that a token belongs to a specific patron.

## Understanding Plausible Deniability

When you generate tokens, there's a calculable probability that any given patron shares their token with at least one other patron in your population. This is your **plausible deniability**.

For example, with 350,000 patrons and 6-character tokens:

> "There's a 1 in 48 chance this token belongs to a different patron."

This matters in legal contexts. If someone demands you identify a patron from a token, you can truthfully say that the token is ambiguous by design.

## Choosing Your Token Size

Larger tokens = fewer collisions = weaker deniability but cleaner analytics.
Smaller tokens = more collisions = stronger deniability but noisier analytics.

Use this table to choose. The "1 in X" number is the chance that any given patron shares their token with someone else:

| Population  | 5 chars     | 6 chars      | 7 chars       |
| ----------- | ----------- | ------------ | ------------- |
| 10,000      | 1 in 105    | 1 in 1,678   | 1 in 26,844   |
| 50,000      | 1 in 21     | 1 in 336     | 1 in 5,369    |
| 100,000     | 1 in 11     | 1 in 168     | 1 in 2,685    |
| 350,000     | 1 in 4      | 1 in 48      | 1 in 767      |
| 500,000     | 1 in 3      | 1 in 34      | 1 in 537      |
| 1,000,000   | 1 in 2      | 1 in 17      | 1 in 269      |
| 2,000,000   | 1 in 1      | 1 in 9       | 1 in 135      |

### Important: Plan for Lifetime, Not Just Current

Your population isn't static. Patrons leave, new patrons join. Over 10-20 years, you may tokenize 2-3x more patron IDs than your current active count.

Consider periodically purging or aggregating old transaction data — this is good library policy regardless, and it helps keep your effective population size manageable. Think about your churn rate and growth trajectory when estimating lifetime population.

**Plan for lifetime population, not current population.**

### Quick Recommendations

| Library Type     | Current Patrons | Lifetime Estimate | Recommended |
| ---------------- | --------------- | ----------------- | ----------- |
| Small branch     | 5k - 30k        | 15k - 100k        | **5 chars** |
| Medium library   | 30k - 500k      | 100k - 1.5M       | **6 chars** |
| Large consortium | 500k+           | 1.5M+             | **7 chars** |

## Usage

```python
from stochastic_pseudonymizer import StochasticPseudonymizer

# Initialize with your secret and token size
pseudonymizer = StochasticPseudonymizer(
    app_secret="your-secret-key-keep-this-safe",
    token_length=6  # hex characters: 5, 6, or 7
)

# Generate a token from a patron ID
token = pseudonymizer.generate_token(patron_id="P-12345")

print(token)  # e.g., "a7f2b3"
```

### What You Need to Keep Secret

- **`app_secret`**: Anyone with this can generate tokens and potentially match them to patron IDs. Guard it carefully.

### What You Can Publish

- **`token_length`**: This is just configuration. Publishing it doesn't compromise privacy.
- **The algorithm**: This library is open source. Security comes from the secret, not obscurity.

## The "Forever" Decision

Once you start generating tokens with a particular configuration, **you cannot change it** without invalidating all existing tokens.

Before you begin:

1. Estimate your lifetime patron population (be generous)
2. Pick your token length from the table above
3. Generate a strong, random `app_secret`
4. Store the secret securely
5. Document your configuration

## How It Works

Under the hood, this uses HMAC-SHA256 to hash the patron ID with your secret, then truncates to the desired length. The math for collision probability comes from the [birthday problem](https://en.wikipedia.org/wiki/Birthday_problem).

The collision probability for any individual is approximately:

```text
P(collision) ≈ population_size / possible_tokens
```

Where `possible_tokens = 16^token_length` (since we use hexadecimal output).

## License

MIT
