def insert_response(conn, cursor, type, link):
    """Insère une réponse dans la table réponse.

    Parameters
    ----------
    type : String
        Type de la réponse.
    link : String
        Lien de la source de la réponse.

    Returns
    -------
    Boolean
        État de la modification
    """
    try:
        cursor.execute(f'Insert into Response values ("{type}", "{link}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_response(cursor, incident_id):
    """Récupère la réponse pour une des attaques.

    Parameters
    ----------
    incident_id : Int
        ID de l'attaque.

    Returns
    -------
    Réponse SQL
        Résultat de la requête.
    """
    try:
        cursor.execute(f'Select * from Response join Attacks on Attacks.response = Response.id_resp where Attacks.index = "{incident_id}"')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None
