from flask import Flask

from db import init_database

from routes.agents import agents_bp

from test_agents import test_insert_agent


def create_app():
    """Create a Flask application and add blueprints with all routes.

    Returns
    -------
    app
        the application created
    """
    # Create the default app
    app = Flask(__name__)

    # Add a first blueprints with all routes for the API
    # Take a look at the file ./routes/agents.py to have more
    # details about the routes you have access to.
    app.register_blueprint(agents_bp, url_prefix="/agents")

    # TODO - ADD OTHER BLUEPRINTS

    return app


# Entry point of the application
if __name__ == "__main__":
    app = create_app()
    init_database()
    test_insert_agent()
    app.run(port=5000, debug=False)
