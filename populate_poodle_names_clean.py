from mysql_database_handler import MysqlDatabase

poodle_names_db = "poodle_names" #the database
poodle_names_table = "poodle_names" #the table

#info is the columns in the database with their default values


dbase = MysqlDatabase(db=poodle_names_db)

dbase = MysqlDatabase(host='162.241.24.68',user="mystand6_auser",password="WONPq9x!s0p", db="mystand6_WP92C") #credential for connecting to best poodle mysql database
'''
need to whitelist ip of the local computer connecting to remote database. IP address may need to be updated ocassionally because it changes
'''
def main(): 

    no_update_yet = True  #initial value. marker to show no update yet

    column_to_update = "is_popular"
    input_csv_name = "is_popular2"
    f = open("poodle_names//{}.csv".format(input_csv_name), "r", encoding="utf8")
    is_updateable=True  #set to false if you dont want to update parameters of names
    
    
    name = f.readline()

    while len(name) !=0:
        print(name)
        name = name.strip()
        name = name.upper()

        if not poodle_name_exists(name):
            insert_poodle_name(name)

        if is_updateable:
            if no_update_yet:


                a = input("the database will be update on {}. OK? Ctrl C to abort".format(column_to_update))

                
                no_update_yet = False
            
            update_poodle_name_info(name,column_to_update,"1")  #VERY IMPORTANT TO UPDATE THIS BEFORE RUN!!!

        name = f.readline()

    #print(poodle_name_exists(poodle_names_table,"Sansa"))
    #insert_poodle_name("Lion")
    
    

    dbase.connection.close()


def update_poodle_name_info(name,column,value):

    sql = "UPDATE poodle_names SET {}='{}' WHERE name='{}';".format(column,value,name)
    dbase.run_sql(sql)

def poodle_name_exists(name):
    
    sql = "SELECT name from poodle_names WHERE name = '{}'  ;".format(name)
    #print(sql)
    res = dbase.run_sql(sql)
    if (len(res) > 0):
        return True      
    else:
        return False
def insert_poodle_name(name):
    sql = sql = "INSERT INTO poodle_names (name) VALUES ('{}')".format(name)
    dbase.run_sql(sql)




main()