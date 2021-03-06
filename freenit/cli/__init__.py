import click
from flask.cli import AppGroup
from flask_security.utils import hash_password
from freenit.models.user import User
from peewee_migrate import Router
from peewee_migrate.router import DEFAULT_MIGRATE_DIR

admin_group = AppGroup('admin', short_help='Manage admin users')
migration = AppGroup('migration', short_help='Migration operations')


def register_admin(app):
    @admin_group.command()
    def create():
        try:
            User.get(email='admin@example.com')
        except User.DoesNotExist:
            admin = User(
                email='admin@example.com',
                admin=True,
                active=True,
                password=hash_password('Sekrit'),
            )
            admin.save()

    app.cli.add_command(admin_group)


def register_migration(app):
    router = Router(
        app.db.database,
        migrate_dir=f'{DEFAULT_MIGRATE_DIR}/main',
    )
    #  logs_router = Router(
    #      app.logdb.database,
    #      migrate_dir=f'{DEFAULT_MIGRATE_DIR}/logs',
    #  )

    @migration.command()
    def list():
        print('=== MAIN ===')
        for migration in router.done:
            print(migration)
        #  print('=== LOGS ===')
        #  for migration in logs_router.done:
        #      print(migration)

    @migration.command()
    @click.argument('name')
    def create(name):
        router.create(name, app.models)

    #  @migration.command()
    #  @click.argument('name')
    #  def logs_create(name):
    #      logs_router.create(name, f'{app_name}.logging')

    @migration.command()
    def run():
        router.run()
        #  logs_router.run()

    app.cli.add_command(migration)


def register(app):
    register_admin(app)
    register_migration(app)
