import urllib.parse as urlparse

from api.utils.auth.settings_google import SettingsGoogleOAuth


def google_oauth_redirect_uri() -> str:
    params = {
        "client_id": SettingsGoogleOAuth.CLIENT_ID,
        "redirect_uri": SettingsGoogleOAuth.REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url_encode = urlparse.urlencode(params)
    return f"{SettingsGoogleOAuth.RECEIVE_CODE}?{url_encode}"
