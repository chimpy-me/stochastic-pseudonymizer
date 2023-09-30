
# StochasticPseudonymizer

A class to generate pseudonymous tokens based on Personally Identifiable Information (PII) with a desired level of deliberate ambiguity introduced via controlled collision probabilities.

The mechanism is designed to balance data utility with privacy considerations. By adjusting the number of bits used from a hash output based on the desired collision probability and population size, a level of uncertainty is introduced. This ensures both data protection and utility for statistical analysis.

**!!!CAUTION!!!:** Adjusting ANY of the initialization values after you have started using this method will invalidate old pseudonymized data. Always maintain consistent settings for a given dataset to ensure reproducibility.

## Attributes

- **app_secret (str):** A secret application key used for salt generation in the hashing process. Protecting this key is crucial for the security of the pseudonymization.
- **population_size (int):** The total number of distinct items intended to be hashed. Default is set to 300,000.
- **target_probability (float):** The desired collision probability indicating the likelihood that two items from the `population_size` will produce the same hash value. Default is set to 0.99999 (almost 100%).
- **iterations (int):** The number of iterations used in the PBKDF2 hashing mechanism to enhance security and deter brute-force attacks. Default is set to 100,000.
- **num_bins (int):** The number of hash values or bins calculated based on the desired collision probability and population size.
- **num_bits (int):** The number of bits required to represent the number of bins.
- **num_bytes (int):** The byte length of the hash output determined by the number of bits.

## Methods

### calculate_num_bins

A static method to compute the number of bins based on the population size and desired collision probability.

#### Parameters

- **population_size (int):** The total number of distinct items intended to be hashed. Represents data points like user IDs, names, or any other data to pseudonymize.
- **target_probability (float):** The desired collision probability. Represents the likelihood that at least two items from the `population_size` will produce the same hash value.

#### Returns

- **int:** The estimated number of bins required to achieve the desired collision probability.

### generate_token

Produce a pseudonymous token based on PII, the app secret, and additional salt data.

#### Parameters

- **pii (str/int):** The Personally Identifiable Information intended for pseudonymization.
- **patron_record (dict):** A record containing information about the patron. This method uses 'id' and 'createdDate' fields from the record for salt generation.

#### Returns

- **str:** A base64 encoded token string that represents the pseudonymized version of the PII.

## Usage

Initialize the pseudonymizer with the desired settings and then use the `generate_token` method to create pseudonymous representations of the provided PII data.

```python
from stochastic_pseudonymizer import StochasticPseudonymizer

# Initialize the pseudonymizer 
pseudonymizer = StochasticPseudonymizer(
    app_secret="secret"
)

# Generate a token from PII and patron record
token = pseudonymizer.generate_token(
    pii="John Doe",
    patron_record={"id": 123, "createdDate": "2023-09-30"}
)

print(token)  # EtiiIw
```
