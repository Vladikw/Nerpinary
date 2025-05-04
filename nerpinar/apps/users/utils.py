from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random


def generate_and_store_verification_code(session):
    """
    Генерирует случайный шестизначный код подтверждения и сохраняет его в сессии вместе с текущим временем.
    Это используется для проверки email при регистрации.
    """
    code = str(random.randint(100000, 999999))  # Создание случайного кода
    now = datetime.now().isoformat()  # Текущее время в ISO-формате
    # Сохраняем код и время его создания в сессию
    session['verification_code'] = code
    session['verification_created_at'] = now
    session['last_resend_at'] = now  # Отметка, когда был отправлен последний код
    return code


def clear_verification_session(session):
    """
    Удаляет все временные данные из сессии, связанные с подтверждением регистрации.
    Обычно вызывается после успешной активации аккаунта.
    """
    for key in ['verification_code', 'pending_user_id', 'verification_created_at', 'last_resend_at']:
        session.pop(key, None)  # Безопасно удаляем, даже если ключа нет


def get_resend_limit_info(session, limit_minutes=1):
    """
    Проверяет, прошло ли достаточно времени для повторной отправки кода подтверждения.
    Возвращает кортеж:
      - True, если можно отправить;
      - False, если ещё рано и строку с оставшимся временем.
    """
    last_resend_at_str = session.get('last_resend_at')
    can_resend = True
    remaining = None

    if last_resend_at_str:
        last_resend_at = datetime.fromisoformat(last_resend_at_str)
        time_left = timedelta(minutes=limit_minutes) - (datetime.now() - last_resend_at)
        if time_left > timedelta(seconds=0):
            # Если время не вышло — запрещаем повторную отправку
            remaining = str(time_left).split('.')[0]  # Убираем миллисекунды
            can_resend = False

    return can_resend, remaining


def get_pending_user_or_redirect(request):
    """
    Пытается получить пользователя, который ещё не подтвердил регистрацию.
    Если не удалось — возвращает редирект на страницу регистрации.
    Используется для проверки email при подтверждении или повторной отправке кода.
    """
    user_id = request.session.get('pending_user_id')
    if not user_id:
        messages.error(request, 'Сессия истекла. Зарегистрируйтесь заново.')
        return None, redirect('users:register')

    try:
        user = User.objects.get(id=user_id)
        return user, None  # Успешно найден пользователь
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return None, redirect('users:register')


def send_verification_email(user, code, subject=None):
    """
    Отправляет письмо с кодом подтверждения на почту пользователя.
    Используется после регистрации или при повторной отправке кода.
    """
    if subject is None:
        subject = 'Код подтверждения регистрации на Nerpinary'

    from_email = settings.DEFAULT_FROM_EMAIL  # Почта отправителя (из настроек Django)
    to_email = [user.email]  # Адрес получателя

    # Текстовое и HTML-содержимое письма
    text_content = f'Ваш код подтверждения: {code}'
    html_content = f'''
        <html>
            <body>
                <p>Здравствуйте, {user.username}!</p>
                <p>Ваш код подтверждения:</p>
                <h2>{code}</h2>
                <p>Введите его на сайте, чтобы завершить регистрацию.</p>
            </body>
        </html>
    '''

    # Создание и отправка письма
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")  # Прикрепляем HTML-версию
    msg.send()
