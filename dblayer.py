import json
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def start_db():
    mydb = mysql.connector.connect(
        host=config['DB_CONFIG']['host'],
        user=config['DB_CONFIG']['user'],
        password=config['DB_CONFIG']['password'],
        database=config['DB_CONFIG']['database']
    )
    return mydb


def truncate_table():
    try:
        mydb = start_db()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("TRUNCATE TABLE url_db")
        return 1
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        mydb.close()


def get_all_records():
    try:
        mydb = start_db()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM url_db")

        result = cursor.fetchall()
        return json.dumps(result)
    except Exception as e:
        print('Exception occurred in dblayer the trace {}'.format(e))
        return 'Exception occurred'
    finally:
        cursor.close()
        mydb.close()


def get_record_by_id(id):
    try:
        mydb = start_db()
        cursor = mydb.cursor(dictionary=True)
        sql = 'SELECT * FROM url_db WHERE id = {}'.format(id)
        cursor.execute(sql)
        result = cursor.fetchall()
        return json.dumps(result)
    except Exception as e:
        print('Exception occurred in dblayer the trace {}'.format(e))
        return 'Exception occurred'
    finally:
        cursor.close()
        mydb.close()


def update_record(id, url, update=True):
    try:
        mydb = start_db()
        cursor = mydb.cursor()
        if update:
            sql = "UPDATE url_db SET URL = \'{}\' WHERE id = {}".format(url, id)
        else:
            sql = "DELETE FROM url_db WHERE id = {}".format(id)
        cursor.execute(sql)
        mydb.commit()
        return cursor.rowcount
    except Exception as e:
        print('Exception occurred in dblayer the trace {}'.format(e))
        return 0
    finally:
        cursor.close()
        mydb.close()


def insert_record(url):
    try:
        mydb = start_db()
        cursor = mydb.cursor()
        sql = "INSERT INTO url_db (URL) VALUES (%s)"
        cursor.execute(sql, (url,))
        mydb.commit()
        return cursor.rowcount
    except Exception as e:
        print('Exception occurred in dblayer the trace {}'.format(e))
        return 0
    finally:
        cursor.close()
        mydb.close()


def check_for_url(url):
    try:
        mydb = start_db()
        cursor = mydb.cursor(dictionary=True)
        sql = 'SELECT * FROM url_db WHERE url = \'{}\''.format(url)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print('Exception occurred in dblayer the trace {}'.format(e))
        return 0
    finally:
        cursor.close()
        mydb.close()
