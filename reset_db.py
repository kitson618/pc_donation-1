from app import create_app, SQLAlchemy

app = create_app()
db = SQLAlchemy(app)

db.reflect()
db.drop_all()
