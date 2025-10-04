from dao.db_connection import DBConnection

with DBConnection().connection as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM defaultdb."Type";')
        rows = cur.fetchall()
        for row in rows:
            print(row)