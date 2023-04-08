import psycopg2


def writeTable(id, value):
    """ Connect to the PostgreSQL database server """
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="464254")

    try:
        print('Connecting to the PostgreSQL database...')

        cur = conn.cursor()

        cur.execute("""UPDATE public.qwert SET name2=array_append(name2, '{}') WHERE id = {};""".format(value, id))

        conn.commit()
        conn.close()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


writeTable(1, 'Nazar')
