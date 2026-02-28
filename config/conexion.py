import psycopg2

def conectar():
    try:
        return psycopg2.connect(
            host="localhost",
            user="postgres",
            password="Mortadela705",
            database="sena_food",
            port="5432"
        )
    except:
        return None
