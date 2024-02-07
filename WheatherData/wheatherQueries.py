# This code was written by Noah and Warren

import psycopg2

def test_connection():

    conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="dawsonj2",
    user="dawsonj2",
    password="eyebrow529redm")

    if conn is not None:
        print( "Connection Worked!" )
    else:
        print( "Problem with Connection" )

    return None

def get_everything_from(table):
    try:
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="dawsonj2",
        user="dawsonj2",
        password="eyebrow529redm")

        cur = conn.cursor()

        sql = """
        SELECT * FROM """+table+""";
        """
        
        cur.execute(sql)
        rows = cur.fetchall()

        if(rows is not None):
            for row in rows:
                print(row)
        else:
            print("No instance found")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def main():
    test_connection()
    get_everything_from("country")


main()
