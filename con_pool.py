import psycopg2.pool

DATABASE_URL = "postgresql://bond:hkJBMZZaRBmmcaGiKDM8rg@project-8970.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/project?sslmode=require"
connection_pool = None

def start_connection_pool():
    try:
        global connection_pool
        print("Creating Connection to database...")
        connection_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, dsn=DATABASE_URL)
        print("Connection pool created successfully")
        return
    except psycopg2.OperationalError as e:
        print("Could not connect to database:", e)
        return None

def close_connection_pool():
    print("Disconnectig from Database...")
    global connection_pool
    if connection_pool:
        connection_pool.closeall()  
    print("Connection to Database has been severed")

def get_connection():
    return connection_pool.getconn()

def release_connection(connection):
    connection_pool.putconn(connection)