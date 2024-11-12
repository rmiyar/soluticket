from django.apps import AppConfig

class UsersConfig(AppConfig):  # Asegúrate de que el nombre coincida con el de tu app
    name = 'users'  # Usa el nombre de tu aplicación aquí

    def ready(self):
        import users.signals  # Importa las señales al iniciar la aplicación
