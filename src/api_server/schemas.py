# We might not need schemas as strictly as in FastAPI.
# But let's keep a simple class or two if needed.

class TokenResponse:
    def __init__(self, access_token, token_type, expires_in, scope=None):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope