import hmac
import hashlib


class StochasticPseudonymizer:
    """
    Generate pseudonymous tokens from patron IDs with built-in plausible
    deniability through intentional hash collisions.

    Args:
        app_secret: Secret key for token generation. Keep this safe.
        token_length: Number of hex characters in output (1-32). Recommended:
                      5 for small libraries (up to ~100k lifetime patrons)
                      6 for medium libraries (up to ~1.5M lifetime patrons)
                      7 for large consortia (up to ~25M lifetime patrons)
    """

    def __init__(self, app_secret: str, token_length: int = 6):
        if not app_secret:
            raise ValueError("app_secret cannot be empty")
        if not isinstance(token_length, int) or not (1 <= token_length <= 32):
            raise ValueError("token_length must be an integer between 1 and 32")

        self._secret = app_secret.encode("utf-8")
        self._length = token_length

    def generate_token(self, patron_id: str) -> str:
        """
        Generate a pseudonymous token for a patron ID.

        Args:
            patron_id: The patron identifier to pseudonymize.

        Returns:
            A hexadecimal token string of length `token_length`.
        """
        digest = hmac.new(
            self._secret,
            str(patron_id).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return digest[: self._length]
