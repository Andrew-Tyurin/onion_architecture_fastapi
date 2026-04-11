from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str
    id: int | None = None


@dataclass
class OAuthAccounts:
    user: User
    provider: str
    provider_user_id: str
    id: int | None = None
