import os
from apps import create_app
from flask.ext.script import Server, Shell, Manager
from flask.ext.stormpath import StormpathManager
# from rhodb.database import db
from apps import db

def create_manager(app, db):
    """ This function creates and configures a Flask-Script manager object.
    """
    manager = Manager(app)

    manager.add_command("runserver", Server())

    def make_shell_context():
        return dict(app=app, db=db)
    manager.add_command("shell", Shell(make_context=make_shell_context))

    return manager

# Expose app & manager
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = create_manager(app, db)

# If main, run the manager.
#
if __name__ == "__main__":
    manager.run()
