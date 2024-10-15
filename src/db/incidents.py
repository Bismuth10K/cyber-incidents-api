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
    try:
        cursor.execute(f'Insert into Attacks values ("{date}", "{name}", "{type}", "{isConfirmed}", "{attacker_affiliation}", NULL, "{response_type}", "{target_name}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_incident(cursor, incident_name):
    try:
        cursor.execute(f'Select * from Attacks where Title = "{incident_name}"')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None


def update_incident_attacker(conn, cursor, incident_name, new_attacker_affilication):
    try:
        cursor.execute(f"Update Attacks set group_attackers = '{new_attacker_affilication}' where Title = '{incident_name}'")
        conn.commit()
    except Exception as e:
        print(e)
        return False


def update_incident_response(incident_name, new_response_type):
    # TODO
    pass


def add_incident_target(incident_name, target_name_to_add):
    # TODO
    pass


def remove_incident_target(incident_name, target_name_to_remove):
    # TODO
    pass


def add_incident_source(incident_name, source_link):
    # TODO
    pass


def remove_incident_source(incident_name, source_link):
    # TODO
    pass
