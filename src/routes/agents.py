from flask import Blueprint, request, jsonify

from db import get_db_connexion, close_db_connexion

import db.agents

agents_bp = Blueprint("agents", __name__)


@agents_bp.route("/", methods=["GET"])
def get_all_agents():
    """Fetch all agents from the database.

    Returns
    -------
    status_code
        200 by default if no error occured
        500 if an error occured while fetching the agents
    data
        agents as a json if no error occurs (can be empty if no agents)
        an error message if an error occured while fetching the agents.
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    all_agents = db.agents.get_agents(cursor)
    if all_agents == None:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return "Error: while fetching agents", 500
    conn.commit()
    close_db_connexion(cursor, conn)
    return jsonify({"agents": [dict(agent)["username"] for agent in all_agents]})


@agents_bp.route("/<agent_username>", methods=["GET"])
def get_agent(agent_username):
    """Fetch a single agent from the database based on its username.

    Parameters
    ----------
    agent_username
        username of the agent (as defined in the database)

    Returns
    -------
    data
        agent as a json if the agent is in the database
        an error message "This agent does not exists" if the agent requested
            is not in the database
        an error message "Error: while fetching agent" if an error occured
            while fetching the agent.
    status_code
        200 if the agent is correctly fetched
        404 if the query to the database was a success but the agent
                is not in the database
        500 if an error occured while fetching the agent
    """
    # TODO
    return jsonify({"message": "TODO"})


@agents_bp.route("/<agent_username>", methods=["PATCH"])
def patch_password(agent_username):
    """Patch the password of an agent.
    The password must be passed in the data of the POST request.

     Parameters
     ----------
     agent_username
         username of the agent (as defined in the database)

     Returns
     -------
     data
         agent as a json if the agent is in the database
         a message "Password not provided" if the password is not in
             the request
         an error message "Error: while updating password" if an error
             occured while updating the password.
     status_code
         200 if the password is correctly modified
         404 if no password is provided in the request
         500 if an error occured while updating the password
    """
    # TODO
    return jsonify({"message": "TODO"})


@agents_bp.route("/", methods=["POST"])
def add_agent():
    """Add an agent to the database.
    The username and password must be passed in the data of the POST request.

    Returns
    -------
    data
        a message "Done" if the agent is correctly added
        a message "Username or password not provided" if the password or
            username is not in the data of the POST request
        an error message "Error: while adding a new agent" if an error occured
            while updating the password
    status_code
        200 if the agent was added to the database
        404 if no username and password are provided in the request
        500 if an error occured while updating the password
    """
    # TODO
    return jsonify({"message": "TODO"})
