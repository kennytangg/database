import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def get_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def run_query(query, params=None, fetch=False):
    """Execute an SQL query. If fetch is True, return all rows as a list of dicts. if not commit the query and return None."""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        cursor.execute(query, params or ())

        if fetch:
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return None
    except Error as e:
        print(f"Error executing query: {e}")
        if conn:
            conn.close()
        return None


# Test if database connection works
def test_connection():
    conn = get_connection()
    if conn:
        print("Database connection successful!")
        conn.close()
        return True
    else:
        print("Database connection failed!")
        return False


if __name__ == "__main__":
    test_connection()
