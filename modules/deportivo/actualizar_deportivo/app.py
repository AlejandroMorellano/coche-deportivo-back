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

        entity_id = payload['id']
        marca = payload['marca']
        modelo = payload['modelo']
        velocidadMaxima = float(payload['velocidadMaxima'])
        peso = float(payload['peso'])

        # Start transaction
        conn.autocommit = False

        # Find entity by id
        cur.execute("SELECT * FROM deportivo WHERE id = %s", (entity_id,))
        entity = cur.fetchone()

        if not entity:
            return {
                "statusCode": 204,
                'headers': headers,
                "body": json.dumps({"message": "Coche Deportivo no encontrado"})}

        # Update entity
        cur.execute("UPDATE deportivo SET marca = %s, modelo = %s, velocidadMaxima = %s, peso = %s WHERE id = %s",
                    (marca, modelo, velocidadMaxima, peso, entity_id))

        # Commit query
        conn.commit()
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': "Coche Deportivo actualizado."})}
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
