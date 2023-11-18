# database
import psycopg2

def connect_to_db(hostname, database,username, password, port_id,data,fnr):
    # db credentials
    hostname = hostname
    database = database
    username = username
    password = password
    port_id = port_id
    
    
    
    con = psycopg2.connect(host=hostname, dbname=database,
                            user=username, password=password, port=port_id)
    if con:
        connect_status=True
        print(connect_status)
    else:
        connect_status=False
        
        print("Connection",connect_status)
    cur = con.cursor()    
    # return cur
                            
    delete_script="delete from public.location_data_fois where fnr='"+fnr+"'"

    cur.execute(delete_script)
    # save transactions
    con.commit()
   
   

    for d in data:
        print(d)
        insert_script= '''INSERT INTO public.location_data_fois(
	 fnr, location_name, type_location, status)
	VALUES ( %s, %s, %s, %s);'''
        insert_values=(d[0],d[1],d[2],d[3])
        cur.execute(insert_script,insert_values)
        
        # save transactions
        con.commit()
        
    update_column="UPDATE location_data_fois SET station_code = SUBSTRING(location_name FROM 1 FOR POSITION('(' IN location_name) - 1);"
        
    cur.execute(update_column)
    con.commit()
   
    
# connect_to_db("karma-db.neebal.com", "pmi_db","pmi_web_user", "G@Rtav#2x52f", 5432,dd,"23061821867")   

# delete_data(connect_to_db('tools.neebal.com','pmi_db','pmi_web_user','G@Rtav#2x52f',7026))

# try:
#     connect_to_db('karma-db.neebal.com','pmi_db','pmi_web_user','G@Rtav#2x52f',5432,final_data)
# except Exception as er:
#     print(er)

