def insert_incident(
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
    # TODO
    pass


def get_incident(incident_name):
    # TODO
    pass


def update_incident_attacker(incident_name, new_attacker_affilication):
    # TODO
    pass


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
