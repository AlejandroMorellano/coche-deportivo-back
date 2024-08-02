import json
from psycopg2.extras import RealDictCursor
from connect_db import get_db_connection

headers = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE, OPTIONS'
}

def lambda_handler(_event, _context):
    conn = None
    cur = None
    try:
        # Get database connection
        conn = get_db_connection()

        # Create cursor
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Find all deportivo entries
        cur.execute("SELECT * FROM deportivo")
        entities = cur.fetchall()

        if not entities:
            return {
                "statusCode": 204,
                'headers': headers,
                "body": json.dumps({"message": "No hay Coches Deportivos registrados"})}

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'data': entities})}
    except Exception as e:
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
