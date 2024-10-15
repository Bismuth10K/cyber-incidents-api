def insert_response(conn, cursor, type, link):
    try:
        cursor.execute(f'Insert into Response values ("{type}", "{link}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_response(cursor, incident_id):
    try:
        cursor.execute(f'Select * from Response join Attacks on Attacks.response = Response.id_resp where Attacks.index = "{incident_id}"')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None
