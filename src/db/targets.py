def insert_target(conn, cursor, target_name, category):
    """Insère une victime.

    Parameters
    ----------
    target_name : String
        Nom victime.
    category : String
        Secteur de la victime.

    Returns
    -------
    Boolean
        État de la modification
    """
    try:
        cursor.execute(f'Insert into Victims values ("{target_name}", "{category}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_targets(cursor):
    """Recupère toutes les victimes.

    Returns
    -------
    Liste de Strings
        Liste des victims.
    """
    try:
        query = """Select DISTINCT name_victim from Victims"""
        
        cursor.execute(query)
        targets = [row[0] for row in cursor.fetchall()]
        return targets
    except Exception as e:
        # Nous laissons la gestion de l'erreur à la fonction appelante
        raise Exception(f"Erreur lors de la récupération des sources : {str(e)}")
