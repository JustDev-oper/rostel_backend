from typing import Protocol
class CRMConnector(Protocol):
    """Contract for a future approved CRM adapter; no external calls are implemented."""
    def push_deal(self, deal: dict) -> str: ...
class TwoFactorProvider(Protocol):
    """Contract for future 2FA provider; secrets and OTP delivery stay outside this application."""
    def begin_challenge(self, user_id: str) -> str: ...
