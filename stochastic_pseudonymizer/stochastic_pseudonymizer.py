import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import constant_time
import math
import os


class StochasticPseudonymizer:
  def __init__(
      self,
      app_secret,                 # protect this secret
      population_size=300_000,    # number of items
      target_probability=0.99999, # target collision probability
      iterations=100_000          # PBKDF2 iterations
  ):

    self.app_secret = app_secret
    self.iterations = iterations

    # Calculate the number of bins for the desired collision 
    # probability
    self.num_bins = int(
        self.calculate_num_bins(
            population_size,
            target_probability
        )
    )

    # Calculate the number of bits required
    self.num_bits = math.ceil(math.log2(self.num_bins))
    # Calculate the number of bytes required for the given 
    # number of bits
    self.num_bytes = (self.num_bits + 7) // 8

  @staticmethod
  def calculate_num_bins(population_size, target_probability):
    return population_size**2 / \
        (-2 * math.log(1 - target_probability))

  def generate_token(self, pii, patron_record):
    # Calculate the salt using PII, app_secret, and patron record 
    # fields
    salt = (
        str(pii)
        + self.app_secret
        + str(patron_record['id'])
        + str(patron_record['createdDate'])
    ).encode('utf-8')

    # PBKDF2 hashing with length determined by self.num_bytes
    hash_value = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=self.num_bytes,
        salt=salt,
        iterations=self.iterations,
        backend=default_backend()
    ).derive(
        str(pii).encode('utf-8')
    )

    # Convert the hash value to an integer and take it modulus
    # num_bins
    token_value = int.from_bytes(
        hash_value,
        byteorder='big'
    ) % self.num_bins

    # Convert the integer token value to bytes and then to a base64 
    # string
    return base64.b64encode(
        token_value.to_bytes(
            max(1, (token_value.bit_length() + 7) // 8), byteorder='big'
        )
    ).decode('utf-8').rstrip('=')