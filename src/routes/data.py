from flask import Blueprint, request, jsonify

data_bp = Blueprint("data", __name__)


@data_bp.route("/sources")
def get_sources():
    """Get all sources in the database.

    Returns
    -------
    data
        all sources in the database
        an error message "Error: while fetching sources" if an error occured
            while fetching the sources.
    status_code
        200 if the sources are correctly fetched
        500 if an error occured while fetching the sources
    """
    # TODO
    return jsonify({"message": "TODO"})


@data_bp.route("/targets")
def get_targets():
    """Get all targets in the database.

    Returns
    -------
    data
        all targets in the database
        an error message "Error: while fetching targets" if an error occured
            while fetching the targets.
    status_code
        200 if the targets are correctly fetched
        500 if an error occured while fetching the targets
    """
    # TODO
    return jsonify({"message": "TODO"})


@data_bp.route("/attackers")
def get_attackers():
    """Get all attackers in the database.

    Returns
    -------
    data
        all attackers in the database
        an error message "Error: while fetching attackers" if an error occured
            while fetching the attackers.
    status_code
        200 if the attackers are correctly fetched
        500 if an error occured while fetching the attackers
    """
    # TODO
    return jsonify({"message": "TODO"})


@data_bp.route("/responses")
def get_responses():
    """Get all responses in the database.

    Returns
    -------
    data
        all responses in the database
        an error message "Error: while fetching responses" if an error occured
            while fetching the responses.
    status_code
        200 if the responses are correctly fetched
        500 if an error occured while fetching the responses
    """
    # TODO
    return jsonify({"message": "TODO"})
