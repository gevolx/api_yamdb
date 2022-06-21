"""
ASGI config for YaMDb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')

application = get_asgi_application()
