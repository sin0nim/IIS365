from app import create_app
from app.models import Users, House, Purchase, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'House': House, 'Purchase': Purchase}

