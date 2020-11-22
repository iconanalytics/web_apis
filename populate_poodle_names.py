from mysql_database_handler import MysqlDatabase

poodle_names_db = "poodle_names" #the database
poodle_names_table = "poodle_names" #the table

#info is the columns in the database with their default values
info = {
    "is_male":'0',
    "is_female":'0',
    "is_standard":'0',
    "is_miniature":'0',
    "is_toy":'0',
    "is_apricot":'0',
    "is_black":'0',
    "is_blue":'0',
    "is_brown":'0',
    "is_cafe_au_lait":'0',
    "is_cream":'0',
    "is_gray":'0',
    "is_red":'0',
    "is_silver":'0',
    "is_silver_beige":'0',
    "is_white":'0',
    "is_phantom":'0',
    "is_parti":'0',
    "is_tuxedo":'0',
    "is_mismarks":'0',
    "is_popular":'0',
    "is_unique":'0',
    "is_classy":'0',
    "is_fancy":'0',
    "is_funny":'0',
    "is_french":'0',
    "is_human_name":'0',
    "is_animal_name_inspired":'0',
    "is_movie_inspired":'0',
    "is_tv_show_inspired":'0'


}

dbase = MysqlDatabase(db=poodle_names_db)

def main():

    #print(poodle_name_exists(poodle_names_table,"Sansa"))
    #insert_poodle_name_info(poodle_names_table,"John",info)
    update_poodle_name_info()

def update_poodle_name_info():

    sql = "UPDATE poodle_names SET {}='{}' WHERE name='{}';".format('is_male','1',"Alex")
    dbase.run_sql(sql)

def poodle_name_exists(table,name):
    
    sql = "SELECT name from {} WHERE name = '{}'  ;".format(table,name)
    print(sql)
    res = dbase.run_sql(sql)
    if (len(res) > 0):
        return True      
    else:
        return False
def insert_poodle_name_info(table,name,info):
    sql = "INSERT INTO {} (name,\
                    is_male 	,\
                    is_female 	,\
                    is_standard 	,\
                    is_miniature 	,\
                    is_toy 	,\
                    is_apricot 	,\
                    is_black 	,\
                    is_blue 	,\
                    is_brown 	,\
                    is_cafe_au_lait 	,\
                    is_cream 	,\
                    is_gray 	,\
                    is_red 	,\
                    is_silver 	,\
                    is_silver_beige 	,\
                    is_white 	,\
                    is_phantom 	,\
                    is_parti 	,\
                    is_tuxedo 	,\
                    is_mismarks 	,\
                    is_popular 	,\
                    is_unique 	,\
                    is_classy 	,\
                    is_fancy 	,\
                    is_funny 	,\
                    is_french 	,\
                    is_human_name 	,\
                    is_animal_name_inspired 	,\
                    is_movie_inspired 	,\
                    is_tv_show_inspired 	) \
            VALUES ('{}'    ,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	,\
                    '{}'	);".format(table,name,info["is_male"],
                                                    info["is_female"],
                                                    info["is_standard"],
                                                    info["is_miniature"],
                                                    info["is_toy"],
                                                    info["is_apricot"],
                                                    info["is_black"],
                                                    info["is_blue"],
                                                    info["is_brown"],
                                                    info["is_cafe_au_lait"],
                                                    info["is_cream"],
                                                    info["is_gray"],
                                                    info["is_red"],
                                                    info["is_silver"],
                                                    info["is_silver_beige"],
                                                    info["is_white"],
                                                    info["is_phantom"],
                                                    info["is_parti"],
                                                    info["is_tuxedo"],
                                                    info["is_mismarks"],
                                                    info["is_popular"],
                                                    info["is_unique"],
                                                    info["is_classy"],
                                                    info["is_fancy"],
                                                    info["is_funny"],
                                                    info["is_french"],
                                                    info["is_human_name"],
                                                    info["is_animal_name_inspired"],
                                                    info["is_movie_inspired"],
                                                    info["is_tv_show_inspired"]
                                                    )
    #print(sql)
    dbase.run_sql(sql)




main()