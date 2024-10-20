from flask import Blueprint, jsonify, request
from db import get_db_connexion, close_db_connexion
import json
from utils import token_required

incidents_bp = Blueprint("incidents", __name__)


@token_required
@incidents_bp.route("/<int:incident_id>")
def get_incident(incident_id):
    """Get an incident in the database based on its incident id.

    Parameters
    ----------
    incident_id
        id of the incident to get

    Returns
    -------
    data
        all data about the incident if correctly fetched
        a message "Incident does not exist" if the incident is not found in
            the database.
        an error message "Error: while fetching the incident" if an error
            occured while fetching the incident.
    status_code
        200 if the incident is correctly fetched
        404 if the incident does not exist in the database
        500 if an error occured while fetching the incident
    """
    try:
        conn = get_db_connexion()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Attacks WHERE id_attack = {incident_id}")
        incident = [elem for elem in cursor.fetchone()]
            
        if incident:
            return jsonify(incident), 200
        else:
            return jsonify({"message": "Incident does not exist"}), 404
    except Exception as e:
        return jsonify({"message": f"Error: while fetching the incident - {str(e)}"}), 500


@token_required
@incidents_bp.route("/<int:incident_id>/assign", methods=["POST"])
def assign_incident(incident_id):
    """Assign an incident to an agent.

    Parameters
    ----------
    incident_id
        id of the incident to get

    Returns
    -------
    data
        a message "Done" if the agent is assigned correctly to the incident.
        a message "No agent username provided for assignment" if no the field
            username is not found in the request data
        a message "Incident does not exist" if the incident is not found in
            the database.
        a message "Agent does not exist" if the agent is not found in the
            database
        an error message "Error: while fetching the incident" if an error
            occured while fetching the incident.
    status_code
        200 if the agent is assigned correctly to the incident.
        400 if no the field username is not found in the request data
        404 if the incident does not exist in the database
        404 if the agent does not exist in the database
        500 if an error occured while fetching the incident
    """
    try:
        text = request.get_data("text")
        username = json.loads(text.decode('utf-8')).get("username")
        if not username:
            return jsonify({"message": "No agent username provided for assignment"}), 400

        conn = get_db_connexion()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM Attacks WHERE id_attack = "{incident_id}"')
        if not cursor.fetchone():
            return jsonify({"message": "Incident does not exist"}), 404

        cursor.execute(f'SELECT * FROM Agents WHERE username = "{username}"')
        if not cursor.fetchone():
            return jsonify({"message": "Agent does not exist"}), 404

        cursor.execute(f'UPDATE Attacks SET username_agents = "{username}" WHERE id_attack = {incident_id}')
        cursor.commit()

        return jsonify({"message": "Done"}), 200

    except Exception as e:
        return jsonify({"message": f"Error: while assigning the incident - {str(e)}"}), 500


@token_required
@incidents_bp.route("/<int:incident_id>", methods=["PATCH"])
def update_incident(incident_id):
    """Update an incident in the database based on its incident id.
    The fields to update must be passed in the data of the PATCH request among
    the following (pass any of them):
        - agent_username
        - description
        - type
        - date
        - name
        - isConfirmed
        - response_type

    Parameters
    ----------
    incident_id
        id of the incident to update

    Returns
    -------
    data
        a message "Done" if the incident is updated correctly.
        a message "No field provided for update" if no field is found in the
            data passed in the request
        a message "Incident does not exist" if the incident is not found in
            the database.
        an error message "Error: while updating the incident" if an error
            occured while updating the incident.
    status_code
        200 if the incident is updated correctly
        400 if no field is found in the data passed in the request
        404 if the incident does not exist in the database
        500 if an error occured while updating the incident
    """
    # TODO
    return jsonify({"message": "TODO"})


@token_required
@incidents_bp.route("/<int:incident_id>/add", methods=["POST"])
def add_element_to_incident(incident_id):
    """Add an element to an incident in the database based on its incident id.
    The data to update must be passed in the data of the POST request among
    the following:
        - target
        - source

    Parameters
    ----------
    incident_id
        id of the incident to update

    Returns
    -------
    data
        a message "Done" if the incident is updated correctly.
        a message "No field provided for addition" if no field is found in the
            data passed in the request
        a message "Incident does not exist" if the incident is not found in
            the database.
        an error message "Error: while updating the incident" if an error
            occured while updating the incident.
    status_code
        200 if the incident is updated correctly
        400 if no field is found in the data passed in the request
        404 if the incident does not exist in the database
        500 if an error occured while updating the incident
    """
    try:
        data = request.json
        query = None

        if 'target' in data:
            query = f"UPDATE Attacks SET victim = '{data["target"]}' WHERE id_attack = {incident_id}"
        elif 'source' in data:
            query = f"UPDATE Attacks SET id_src = '{data["source"]}' WHERE id_attack = {incident_id}"

        if not query:
            return jsonify({"message": "No field provided to be added"}), 400

        conn = get_db_connexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Attacks WHERE id_attack = %s", (incident_id,))
        if not cursor.fetchone():
            return jsonify({"message": "Incident does not exist"}), 404
        cursor.execute(query)
        cursor.commit()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Done"}), 200
    
    except Exception as e:
        cursor.rollback()
        return jsonify({"message": f"Error: while updating the incident - {str(e)}"}), 500


@token_required
@incidents_bp.route("/<int:incident_id>/remove", methods=["POST"])
def remove_element_from_incident(incident_id):
    """Remove an element from an incident in the database.
    The data to update must be passed in the data of the POST request among
    the following:
        - target
        - source

    Parameters
    ----------
    incident_id
        id of the incident to update

    Returns
    -------
    data
        a message "Done" if the incident is updated correctly.
        a message "No field provided to be removed" if no field is found in the
            data passed in the request
        a message "Incident does not exist" if the incident is not found in
            the database.
        an error message "Error: while updating the incident" if an error
            occured while updating the incident.
    status_code
        200 if the incident is updated correctly
        400 if no field is found in the data passed in the request
        404 if the incident does not exist in the database
        500 if an error occured while updating the incident
    """
    try:
        data = request.json
        query = None

        if 'target' in data:
            query = f"UPDATE Attacks SET victim = NULL WHERE id_attack = {incident_id}"
        elif 'source' in data:
            query = f"DELETE FROM Attack_sources WHERE id_att = {incident_id}"

        if not query:
            return jsonify({"message": "No field provided to be removed"}), 400

        conn = get_db_connexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Attacks WHERE id_attack = %s", (incident_id,))
        if not cursor.fetchone():
            return jsonify({"message": "Incident does not exist"}), 404
        cursor.execute(query)
        cursor.commit()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Done"}), 200
    
    except Exception as e:
        cursor.rollback()
        return jsonify({"message": f"Error: while updating the incident - {str(e)}"}), 500
