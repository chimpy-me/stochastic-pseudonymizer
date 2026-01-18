import pytest
from stochastic_pseudonymizer import StochasticPseudonymizer


class TestTokenGeneration:
    """Test basic token generation functionality."""

    def test_generates_token(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")
        token = pseudonymizer.generate_token(patron_id="P-12345")

        assert token is not None
        assert isinstance(token, str)

    def test_token_has_correct_length(self):
        for length in [5, 6, 7]:
            pseudonymizer = StochasticPseudonymizer(
                app_secret="test-secret",
                token_length=length,
            )
            token = pseudonymizer.generate_token(patron_id="P-12345")

            assert len(token) == length

    def test_token_is_hexadecimal(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")
        token = pseudonymizer.generate_token(patron_id="P-12345")

        # Should only contain valid hex characters
        assert all(c in "0123456789abcdef" for c in token)


class TestDeterminism:
    """Test that tokens are deterministic."""

    def test_same_input_produces_same_token(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")

        token1 = pseudonymizer.generate_token(patron_id="P-12345")
        token2 = pseudonymizer.generate_token(patron_id="P-12345")

        assert token1 == token2

    def test_separate_instances_produce_same_token(self):
        pseudonymizer1 = StochasticPseudonymizer(app_secret="test-secret")
        pseudonymizer2 = StochasticPseudonymizer(app_secret="test-secret")

        token1 = pseudonymizer1.generate_token(patron_id="P-12345")
        token2 = pseudonymizer2.generate_token(patron_id="P-12345")

        assert token1 == token2


class TestDifferentiation:
    """Test that different inputs produce different tokens."""

    def test_different_patron_ids_produce_different_tokens(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")

        token1 = pseudonymizer.generate_token(patron_id="P-12345")
        token2 = pseudonymizer.generate_token(patron_id="P-67890")

        assert token1 != token2

    def test_different_secrets_produce_different_tokens(self):
        pseudonymizer1 = StochasticPseudonymizer(app_secret="secret-one")
        pseudonymizer2 = StochasticPseudonymizer(app_secret="secret-two")

        token1 = pseudonymizer1.generate_token(patron_id="P-12345")
        token2 = pseudonymizer2.generate_token(patron_id="P-12345")

        assert token1 != token2

    def test_different_token_lengths_produce_different_tokens(self):
        pseudonymizer1 = StochasticPseudonymizer(app_secret="test-secret", token_length=5)
        pseudonymizer2 = StochasticPseudonymizer(app_secret="test-secret", token_length=6)

        token1 = pseudonymizer1.generate_token(patron_id="P-12345")
        token2 = pseudonymizer2.generate_token(patron_id="P-12345")

        # Shorter token should be a prefix of longer token (both from same hash)
        assert token2.startswith(token1)
        assert token1 != token2


class TestValidation:
    """Test input validation."""

    def test_empty_secret_raises_error(self):
        with pytest.raises(ValueError, match="app_secret cannot be empty"):
            StochasticPseudonymizer(app_secret="")

    def test_token_length_must_be_positive(self):
        with pytest.raises(ValueError, match="token_length must be an integer between 1 and 32"):
            StochasticPseudonymizer(app_secret="test-secret", token_length=0)

    def test_token_length_must_not_exceed_maximum(self):
        with pytest.raises(ValueError, match="token_length must be an integer between 1 and 32"):
            StochasticPseudonymizer(app_secret="test-secret", token_length=33)

    def test_token_length_must_be_integer(self):
        with pytest.raises(ValueError, match="token_length must be an integer between 1 and 32"):
            StochasticPseudonymizer(app_secret="test-secret", token_length=6.5)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_numeric_patron_id(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")

        # Should handle numeric IDs by converting to string
        token = pseudonymizer.generate_token(patron_id=12345)

        assert token is not None
        assert len(token) == 6

    def test_empty_patron_id(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret")

        # Empty string is valid (though not recommended)
        token = pseudonymizer.generate_token(patron_id="")

        assert token is not None
        assert len(token) == 6

    def test_minimum_token_length(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret", token_length=1)
        token = pseudonymizer.generate_token(patron_id="P-12345")

        assert len(token) == 1

    def test_maximum_token_length(self):
        pseudonymizer = StochasticPseudonymizer(app_secret="test-secret", token_length=32)
        token = pseudonymizer.generate_token(patron_id="P-12345")

        assert len(token) == 32
