from apps import create_app, config
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

app = create_app(config.ENVI_DEFAULT_KEY)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
