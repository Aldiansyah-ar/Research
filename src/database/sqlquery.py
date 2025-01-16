import psycopg2 
from psycopg2 import sql
import pandas as pd

def create_table(table_name, db_config):
  conn = psycopg2.connect(**db_config)
  cursor = conn.cursor()

  create_table_query = sql.SQL(
        """
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            source VARCHAR(100),
            title TEXT,
            url TEXT,
            content TEXT,
            date VARCHAR(100)
        )
        """
    ).format(table_name=sql.Identifier(table_name))
  
  cursor.execute(create_table_query)
  conn.commit()
  cursor.close()
  conn.close()

def fetch_data(query, db_config):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Execute the SQL query
        cursor.execute(query)
        
        # Fetch all rows from the executed query
        data = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        return data
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def insert_data(df, table_name):
    conn = psycopg2.connect(**db_config)
    with conn.cursor() as cursor:
        # Iterasi per baris pada DataFrame
        for _, row in df.iterrows():
            # Buat dictionary object baris pada DataFrame
            rows = {k: v for k, v in row.to_dict().items()}
            
            # Siapkan kolom dan nilai untuk query
            columns = ', '.join([f'"{column}"' for column in rows.keys()])
            placeholders = ', '.join(['%s'] * len(rows))
            values = list(rows.values())
            
            # Buat query SQL untuk insert
            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """
            # Eksekusi query untuk baris saat ini
            cursor.execute(query, values)

# Example usage
db_config = {
    'dbname': 'news',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

query = '''SELECT * FROM sambo_072022
            WHERE id > 100;'''

data = fetch_data(query, db_config)