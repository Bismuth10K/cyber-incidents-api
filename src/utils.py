import bcrypt
import jwt
import datetime
import configparser
from functools import wraps
from flask import request, jsonify

import db
from db.agents import get_agent

CONFIG_FILE = "./config/config"


def load_config():
    """Loads the application configuration from the configuration file
    into a dictionary.

    Returns
    -------
    A dictionary.
        The application configuration.
    """
    # The dictionary to return.
    config = {}

    with open(CONFIG_FILE, "r") as f:
        line = f.readline()
        while line:
            key, value = line.split(",")
            config[key] = value.strip()
            line = f.readline()
    return config


def hash_password(plain_password):
    """Hash a password

    Parameters
    ----------
    plain_password
        plain password to hash

    Returns
    -------
    hashed_password
        A password hash
    """
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password, salt)
    
    return hashed_password


def check_password(plain_password, hashed_password):
    """Check the plain password against its hashed value

    Parameters
    ----------
    plain_password
        the plain password to check
    hashed_password
        a password hash to check if it is the hash of the plain password

    Returns
    -------
    bool
        True if hashed_password is the hash of plain_password, False otherwise
    """
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)


def check_agent(username, plain_password):
    """Authenticate an agent based on its username and a plain password.

    Parameters
    ----------
    username
        the agent username
    plain_password
        the plain password to check

    Returns
    -------
    bool
        True if the password is associated to the agent, False otherwise
    """
    conn = db.get_db_connexion()
    cursor = conn.cursor()
    res = get_agent(username)
    db.close_db_connexion(cursor, conn)

    return check_password(plain_password, res["password"])


def generate_token(username):
    """Generate a token with a username and an expiracy date of 1h.

    Parameters
    ----------
    username
        the agent username

    Returns
    -------
    token
        the generated token based on the username and an expiracy date of 1h.
    """
    try:
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        payload = {
            'username': username,
            'exp': expiration_time
        }

        token = jwt.encode(payload, load_config()['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        print(f"Error generating token: {e}")
        return None


def check_token(token):
    """Check the validity of a token.

    Parameters
    ----------
    token
        the token to check

    Returns
    -------
    payload
        The payload associated with the token if the token is correctly decoded.
        An error if the token is expired or invalid
    """
    try:
        payload = jwt.decode(token, load_config()['SECRET_KEY'], algorithms=['HS256'])
        
        if datetime.datetime.now(datetime.timezone.utc) > datetime.datetime.fromtimestamp(payload['exp'], datetime.timezone.utc):
            print("Token has expired")
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(f"Error checking token: {e}")
        return None


def token_required(f):
    """A decorator to specify which routes need a token validation."""

    @wraps(f)
    def decorated(*args, **kwargs):
        """Define the behaviour of a route when a token validation is required.
        """
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = check_token(token)
            if not "username" in payload or not "exp" in payload:
                return jsonify({"error": "Invalid token"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated
