import validators


def validate_url(url):
    error_messages = []

    if not url:
        error_messages.append('URL обязателен')
    if not validators.url(url):
        error_messages.append('Некорректный URL')
    if validators.length(url, max=255):
        error_messages.append('URL превышает 255 символов')

    return error_messages
