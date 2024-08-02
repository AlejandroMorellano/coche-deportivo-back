import json
from connect_db import get_db_connection

headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE, OPTIONS'
}

def lambda_handler(event, _context):
    conn = None
    cur = None
    try:
        # Get database connection
        conn = get_db_connection()

        # Create cursor
        cur = conn.cursor()

        # Get payload
        payload = json.loads(event['body'])

        marca = payload['marca']
        modelo = payload['modelo']
        velocidadMaxima = float(payload['velocidadMaxima'])
        peso = float(payload['peso'])

        # Start transaction
        conn.autocommit = False

        # Save new deportivo entry
        cur.execute("INSERT INTO deportivo(marca, modelo, velocidadMaxima, peso) VALUES (%s, %s, %s, %s)",
                    (marca, modelo, velocidadMaxima, peso))

        # Commit query
        conn.commit()
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': "Coche Deportivo creado."})}
    except Exception as e:
        # Handle rollback
        if conn is not None:
            conn.rollback()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})}
    finally:
        # Close connection and cursor
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
