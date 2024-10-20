from flask import Flask
from flask_graphql import GraphQLView
from models import db
from schema import schema

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

# Set up the GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True)
