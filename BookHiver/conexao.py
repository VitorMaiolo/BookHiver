import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="bookhiver",
        user="postgres",
        password="1234"
    )