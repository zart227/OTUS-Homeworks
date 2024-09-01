from starlette.responses import Response
from starlette.requests import Request
from urllib.parse import quote, unquote

# Куки для сообщений
def set_message_cookie(response: Response, message: str, message_type: str):
    print('Set cookies')
    # Кодируем значения перед сохранением в куки
    encoded_message = quote(message)
    encoded_message_type = quote(message_type)
    response.set_cookie(key="message", value=encoded_message, max_age=10*60)  # Действителен 10 минут
    response.set_cookie(key="message_type", value=encoded_message_type, max_age=10*60)  # Действителен 10 минут
    print(f'Message: {message}')
    print(f'Encoded message: {encoded_message}')

def get_message_from_cookie(request: Request):
    print('Get cookies')
    # Декодируем значения при получении из куки
    encoded_message = request.cookies.get("message", "")
    encoded_message_type = request.cookies.get("message_type", "")
    message = unquote(encoded_message)
    message_type = unquote(encoded_message_type)
    print(f'Message: {message}')
    print(f'Encoded message: {encoded_message}')
    return message, message_type