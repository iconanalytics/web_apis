import pymysql


class MysqlDatabase:
    
    def __init__(self,host='127.0.0.1',
                             user='root',
                             password='perfect',
                             db='test_fawole_rsvp'):

        self.connection = pymysql.connect(host,user,password,db)


    def run_sql(self,sql):
        with self.connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            self.connection.commit()
            query_result = cursor.fetchone()
            print(query_result)
            return query_result

    
    def read_db_table(self,table):

        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "select * from  {};".format(table)
            self.run_sql(sql)

    def entry_exists(self,table,col,entry):
        sql = "SELECT ig_user from {} where {} = '{}';".format(table,col,entry)
        query_result = self.run_sql(sql)

        if query_result is not None:
            return True
        else:
            return False


def main():
    dbase = MysqlDatabase(db='poodle_instagram_pages')
    db_table = 'poodle_pages'
    #dbase.read_db_table( 'poodle_pages' )

    sql = "INSERT INTO {} (ig_shortcode, ig_user, schema_name, schema_alternate_name, schema_description, schema_interaction_count,"\
        "ig_user_page_full_name, ig_user_page_bio, comments)"\
        "VALUES ('{}', '{}', 'c', 'd', 'e', '5', 'f', 'g', '')".format('poodle_pages','a','w')

    #dbase.run_sql(sql)
    
    print(dbase.entry_exists('poodle_pages','ig_user','w'))
    