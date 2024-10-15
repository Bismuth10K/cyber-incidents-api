def insert_target(conn, cursor, target_name, category):
    try:
        cursor.execute(f'Insert into Victims values ("{target_name}", "{category}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_targets(cursor):
    try:
        cursor.execute(f'Select DISTINCT name_victim from Victims')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None
