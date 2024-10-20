from flask import jsonify

def insert_source(conn, cursor, link):
    """Insère une source

    Parameters
    ----------
    conn : 
        Comme fonctions dans incidents.
    cursor : 
        Comme fonctions dans incidents.
    link : String
        Liens à rajouter.

    Returns
    -------
    boolean
        État de la modification.
    """
    try:
        cursor.execute(f'Insert into Sources values ("{link}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_sources(cursor):
    """Renvoie toutes les sources sans doublons.

    Parameters
    ----------
    cursor : 
        cf. autres fonctions

    Returns
    -------
    Liste de Strings
        Liste de toutes les sources.
    """
    try:
        query = """Select DISTINCT name_source from Sources"""
        
        cursor.execute(query)
        sources = [row[0] for row in cursor.fetchall()]
        
        return sources
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des sources : {str(e)}")