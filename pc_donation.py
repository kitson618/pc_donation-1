from app import cli, db, create_app
from app.models import User, Teacher, Volunteer, Region

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'teacher': Teacher, 'Volunteer': Volunteer, 'Region': Region}
