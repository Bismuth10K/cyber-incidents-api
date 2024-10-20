from flask import Blueprint, request, jsonify
from db import get_db_connexion, close_db_connexion
from db import sources, targets, attackers


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
    try:
        conn = get_db_connexion()
        cursor = conn.cursor()
        result = sources.get_sources(cursor)
        close_db_connexion(cursor, conn)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"Error: while fetching sources - {str(e)}"}), 500


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
    try:
        conn = get_db_connexion()
        cursor = conn.cursor()
        result = targets.get_targets(cursor)
        close_db_connexion(cursor, conn)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"Error: while fetching sources - {str(e)}"}), 500


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
    try:
        conn = get_db_connexion()
        cursor = conn.cursor()
        result = attackers.get_attackers(cursor)
        close_db_connexion(cursor, conn)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"Error: while fetching attackers - {str(e)}"}), 500

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
    try:
        conn = get_db_connexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Response")
        responses = [[elem for elem in row] for row in cursor.fetchall()]
        close_db_connexion(cursor, conn)
        return jsonify(responses), 200
    except Exception as e:
        return jsonify({"message": f"Error: while fetching responses - {str(e)}"}), 500
