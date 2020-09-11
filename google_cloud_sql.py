import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='perfect',
                             db='test_fawole_rsvp')


with connection.cursor() as cursor:
    # Create a new record
    sql = "select * from  test_rsvp;"
    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchone()
    print(result)