import validators
from urllib.parse import urlparse

def validate_url(url):
    if not validators.url(url):
        return 'Некорректный URL', True
    if not url:
        return 'URL обязателен', True
    if validators.length(url, max=255):
        return 'URL превышает 255 символов', True
    return None, False


def normalize_url(url):
    """Truncates the URL to the <protocol>://<domain name> structure"""
    url_norm = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    return url_norm
