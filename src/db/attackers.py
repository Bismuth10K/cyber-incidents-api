def insert_attacker(conn, cursor, affiliation, sponsor):
    try:
        cursor.execute(f'Insert into grp_attackers values ("{affiliation}", "{sponsor}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def update_attacker_sponsor(conn, cursor, affiliation, sponsor):
    try:
        cursor.execute(f'Update grp_attackers set name_sponsor = "{sponsor}" where name_grp_att = {affiliation}')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_attackers(cursor):
    try:
        cursor.execute(f'Select DISTINCT name_grp_att from grp_attackers')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None
