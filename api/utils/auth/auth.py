import urllib.parse as urlparse

from api.schemas.auth_schemas import GoogleOAuthParseSchema
from api.utils.auth.settings_google import SettingsGoogleOAuth
from domain.entities.user import User, OAuthAccounts
from infrastructure.utils.base_utils import CsrfToken


def google_oauth_redirect_uri() -> str:
    random_token = CsrfToken.create_token
    CsrfToken.tokens.add(random_token)
    params = {
        "client_id": SettingsGoogleOAuth.CLIENT_ID,
        "redirect_uri": SettingsGoogleOAuth.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "consent",
        "state": random_token,
    }
    url_encode = urlparse.urlencode(params)
    return f"{SettingsGoogleOAuth.RECEIVE_CODE}?{url_encode}"


def to_domain_oauth_google(google_user: GoogleOAuthParseSchema) -> OAuthAccounts:
    """data mapper"""
    user = User(name=google_user.name, email=google_user.email)
    oauth_google_user = OAuthAccounts(
        user=user,
        provider="google",
        provider_user_id=google_user.sub
    )
    return oauth_google_user
