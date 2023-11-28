import os
import mysql.connector

config = {
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASS'),
    'host': os.environ.get('MYSQL_HOST'),
    'port': os.environ.get('MYSQL_PORT'),
    'database': os.environ.get('MYSQL_NAME'),
    'raise_on_warnings': True,
}

def query(sql, params=None, single=False):
    from logging_handling import error_logging
    db = None
    cursor = None
    try:
        # db = mysql.connector.connect(**config)
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)
        if params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        if single:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        db.close()
        return result
    except Exception as e:
        if db is not None:
            db.rollback()
        error_logging(e)
    finally:
        if cursor is not None:
            cursor.close()