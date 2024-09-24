from flask import Blueprint, jsonify

incidents_bp = Blueprint("incidents", __name__)


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
    # TODO
    return jsonify({"message": "TODO"})


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
    # TODO
    return jsonify({"message": "TODO"})


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
    # TODO
    return jsonify({"message": "TODO"})


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
    # TODO
    return jsonify({"message": "TODO"})
