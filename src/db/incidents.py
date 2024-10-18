def insert_incident(conn, cursor, 
    name,
    date,
    description,
    type,
    isConfirmed,
    source_links,
    attacker_affiliation,
    target_name,
    response_type,
):
    """Insère une attaque dans la BDD.

    Parameters
    ----------
    conn : 
        Connecteur de la BDD
    cursor : 
        Curseur afin d'executer du code
    name : String
        Nom de l'attaque
    date : String
        Date de l'attaque
    description : String
        Description de l'attaque
    type : String
        Type de l'attaque
    isConfirmed : boolean
        Si l'attaquant est confirmé
    source_links : String
        Liens des sources de l'info de l'attaque
    attacker_affiliation : Int
        Index de l'attaquant dans la table grp_attackers
    target_name : Int
        Index de la victime dans la table Victims
    response_type : Int
        Index de la réponse dans la table Response

    Returns
    -------
    boolean
        True ou False si l'opération a réussi ou non.
    """
    try:
        cursor.execute(f'Insert into Attacks values ("{date}", "{name}", "{type}", "{isConfirmed}", "{attacker_affiliation}", NULL, "{response_type}", "{target_name}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_incident(cursor, incident_name):
    """Renvoie la liste des attaques associées à un nom passé en paramètre.

    Parameters
    ----------
    cursor : 
        Curseur afin d'executer du code dans la BDD.
    incident_name : String
        Nom de l'attaque à retrouver dans la BDD.

    Returns
    -------
    Liste de String
        La liste de toutes les attaques ayant le même nom. Si les données sont bien, il ne devrait y en avoir qu'une.
    """
    try:
        cursor.execute(f'Select * from Attacks where Title = "{incident_name}"')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None


def update_incident_attacker(conn, cursor, incident_name, new_attacker_affilication):
    """Met à jour la table à l'endroit de incident_name afin de changer l'attaquant.

    Parameters
    ----------
    conn : 
        cf. fonctions précédentes.
    cursor : 
        cf. fonctions précédentes
    incident_name : String
        Nom de l'attaque où il faut modifier l'attaquant.
    new_attacker_affilication : Integer
        ID du nouvel attaquant.

    Returns
    -------
    boolean
        True ou False en fonction de si la modification est bien passée ou non.
    """
    try:
        cursor.execute(f"Update Attacks set group_attackers = '{new_attacker_affilication}' where Title = '{incident_name}'")
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_incident_response(conn, cursor, incident_name, new_response_type):
    """Met à jour la table à l'endroit de incident_name afin de changer la réponse.

    Parameters
    ----------
    conn : 
        cf. fonctions précédentes.
    cursor : 
        cf. fonctions précédentes
    incident_name : String
        Nom de l'attaque où il faut modifier l'attaquant.
    new_response_type : Integer
        ID de la nouvelle réponse.

    Returns
    -------
    boolean
        True ou False en fonction de si la modification est bien passée ou non.
    """
    try:
        cursor.execute(f"Update Attacks set response = '{new_response_type}' where Title = '{incident_name}'")
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def add_incident_target(incident_name, target_name_to_add):
    """
    Pas faite car spécifique à une implémentation qui n'est pas la notre.
    """
    # TODO
    pass


def remove_incident_target(incident_name, target_name_to_remove):
    """
    Pas faite car spécifique à une implémentation qui n'est pas la notre.
    """
    # TODO
    pass


def add_incident_source(incident_name, source_link):
    """
    Pas faite car spécifique à une implémentation qui n'est pas la notre.
    """
    # TODO
    pass


def remove_incident_source(incident_name, source_link):
    """
    Pas faite car spécifique à une implémentation qui n'est pas la notre.
    """
    # TODO
    pass
