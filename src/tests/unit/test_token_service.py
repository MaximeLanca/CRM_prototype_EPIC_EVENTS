from src.security.token_service import decode_token

def test_verify_token(valid_token):
    payload = decode_token(valid_token)
    assert payload["sub"] == "1"
