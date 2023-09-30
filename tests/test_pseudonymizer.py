from stochastic_pseudonymizer import StochasticPseudonymizer

# Test general token generation
def test_token_generation():
    # Initialize the pseudonymizer 
    pseudonymizer = StochasticPseudonymizer(
        app_secret="secret"
    )
    token = pseudonymizer.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )

    assert token is not None
    assert isinstance(token, str)

# Different PII Inputs
def test_pseudonymizer_different_pii():
    # Initialize the pseudonymizer 
    pseudonymizer = StochasticPseudonymizer(
        app_secret="secret"
    )

    token1 = pseudonymizer.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )
    token2 = pseudonymizer.generate_token(
        pii="Jane Smith", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )

    assert token1 != token2, "Tokens should be different for different PII"

# Different Patron Records
def test_pseudonymizer_different_patron_record():
    # Initialize the pseudonymizer 
    pseudonymizer = StochasticPseudonymizer(
        app_secret="secret"
    )

    token1 = pseudonymizer.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )
    token2 = pseudonymizer.generate_token(
        pii="John Doe", 
        patron_record={"id": 124, "createdDate": "2023-09-30"}
    )

    assert token1 != token2, "Tokens should be different for different patron records"

# Different App Secrets
def test_pseudonymizer_different_app_secret():
    pseudonymizer = StochasticPseudonymizer(
        app_secret="secret"
    )

    token1 = pseudonymizer.generate_token(pii="John Doe", patron_record={"id": 123, "createdDate": "2023-09-30"})

    pseudonymizer_new_secret = StochasticPseudonymizer(
        app_secret="new_secret"
    )

    token2 = pseudonymizer_new_secret.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )
    assert token1 != token2, "Tokens should be different for different app secrets"

def test_pseudonymizer_different_init_params():
    pseudonymizer = StochasticPseudonymizer(
        app_secret="secret"
    )

    token1 = pseudonymizer.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )

    # Different Initialization Parameters
    pseudonymizer_new_params = StochasticPseudonymizer(
        app_secret="secret", 
        population_size=500_000, 
        target_probability=0.5
    )
    token2 = pseudonymizer_new_params.generate_token(
        pii="John Doe", 
        patron_record={"id": 123, "createdDate": "2023-09-30"}
    )
    
    assert token1 != token2, "Tokens should be different for different initialization parameters"

print("All tests passed!")

# test_pseudonymizer()