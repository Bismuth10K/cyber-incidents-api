def insert_source(conn, cursor, link):
    try:
        cursor.execute(f'Insert into Sources values ("{link}")')
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_sources(cursor):
    try:
        cursor.execute(f'Select DISTINCT name_source from Sources')
        res = cursor.fetchall()
        return res
    except Exception as e:
        print(e)
        return None
