def insert_attacker(conn, cursor, affiliation, sponsor):
    """Insère un attaquant dans la table grp_attackers.

    Parameters
    ----------
    affiliation : String
        Nom de l'attaquant.
    sponsor : String
        L'instance qui sponsorise l'attaquant pour une attaque.

    Returns
    -------
    Boolean
        État de la modification.
    """
    try:
        cursor.execute(f'Insert into grp_attackers values ("{affiliation}", "{sponsor}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_attacker_sponsor(conn, cursor, affiliation, sponsor):
    """Met à jour le sponsor d'un attaquant dans la table.

    Parameters
    ----------
    affiliation : String
        Attaquant à rechercher
    sponsor : String
        Nouveau sponsor

    Returns
    -------
    Boolean
        État de la modification.
    """
    try:
        cursor.execute(f'Update grp_attackers set name_sponsor = "{sponsor}" where name_grp_att = {affiliation}')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_attackers(cursor):
    """Liste de tous les attaquants.

    Returns
    -------
    Liste de Strings
        Liste des attaquants sans doublons.
    """
    try:
        query = """Select DISTINCT name_grp_att from grp_attackers"""
        
        cursor.execute(query)
        sources = [row[0] for row in cursor.fetchall()]
        
        return sources
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des sources : {str(e)}")
