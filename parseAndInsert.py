import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'


def insert2ReviewsTable():
    with open('.//yelp_dataset//yelp_review.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='@1741'")
            cur = conn.cursor()
        except:
            print('Unable to connect to the database!')

        while line:
            data = json.loads(line)
            #Generate the INSERT statement for the cussent business
            #TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statment based on your own table schema ans
            # include values for all businessTable attributes
            sql_str = "INSERT INTO reviewsTable (business_id, stars) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["stars"]) + ");"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to reviewsTABLE failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2BusinessTable():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='@1741'")
            cur = conn.cursor()
        except:
            print('Unable to connect to the database!')
        

        while line:
            data = json.loads(line)
            #Generate the INSERT statement for the cussent business
            #TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statment based on your own table schema ans
            # include values for all businessTable attributes
            sql_state = "INSERT INTO state (state_id) " \
                        "VALUES('" + cleanStr4SQL(data['state'])+ "');"

            try:
                cur.execute(sql_state)
            except:
                print(sql_state)

            sql_city = "INSERT INTO city(state_id,city_name,city_id)" \
                       "VALUES('" + cleanStr4SQL(data['state']) + "','" + cleanStr4SQL(data['city'])+ "','" + \
                       cleanStr4SQL(data['state']) + cleanStr4SQL(data['city']) + "');"

            try:
                cur.execute(sql_city)
            except:
                print(sql_city)

            sql_city_zip = "INSERT INTO cityzip(city_id,zid)" \
                           "VALUES('" + cleanStr4SQL(data['state']) + cleanStr4SQL(data['city']) + "','" + cleanStr4SQL(data['postal_code'])+"');"

            try:
                cur.execute(sql_city_zip)
            except:
                print(sql_city_zip)

            for category in data['categories']:
                sql_category = "INSERT INTO categories(category_name)"\
                            "VALUES('"+cleanStr4SQL(category)+"');"
                sql_businesscategory = "INSERT INTO businesscategory(bid,category_name)"\
                            "VALUES('"+cleanStr4SQL(data['business_id'])+ "','" +cleanStr4SQL(category)+"');"
                try:
                    cur.execute(sql_category)
                except:
                    print(sql_category)

                conn.commit()
                try:
                    cur.execute(sql_businesscategory)
                except:
                    print(sql_businesscategory)
                conn.commit()

            sql_business = "INSERT INTO business (bid,city_id,zipcode_id,name,address,stars,review_count,numcheckins,reviewrating,longitude,latitude) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data['state']) + cleanStr4SQL(data['city']) + "','" + cleanStr4SQL(data["postal_code"]) + "','" + \
                      cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + str(data["stars"]) + "','" + str(data["review_count"]) + \
                      "','0' ,'" + "0' ,'" +str(data["longitude"]) + "','" + str(data["latitude"]) + "');"
            try:
                cur.execute(sql_business)
            except:
                print(sql_business)

            for category in data['categories']:
                sql_businesscategory = "INSERT INTO businesscategory(bid,category_name)"\
                            "VALUES('"+cleanStr4SQL(data['business_id'])+ "','" +cleanStr4SQL(category)+"');"
                try:
                    cur.execute(sql_businesscategory)
                except:
                    print(sql_businesscategory)
                
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2Checkin():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_checkin.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='@1741'")
            cur = conn.cursor()
        except:
            print('Unable to connect to the database!')
        

        while line:
            data = json.loads(line)
            count_checkin = 0

            for time in data['time']:
                for day in data['time'][time]:
                    count_checkin += (data['time'][time][day])

            sql_state = "INSERT INTO check_in (bid,checkin_count) " \
                        "VALUES('" + cleanStr4SQL(data['business_id'])+ "','" + str(count_checkin)+"');"

            try:
                cur.execute(sql_state)
            except:
                print(sql_state)
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

def insert2Review():
    #reading the JSON file
    with open('.//yelp_dataset//yelp_review.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('.//yelp_dataset//yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='@1741'")
            cur = conn.cursor()
        except:
            print('Unable to connect to the database!')
        

        while line:
            data = json.loads(line)

            sql_state = "INSERT INTO reviews (bid,stars,text) " \
                        "VALUES('" + cleanStr4SQL(data['business_id'])+ "','" + str(data['stars'])+"','" + cleanStr4SQL(data['text'])+"');"

            try:
                cur.execute(sql_state)
            except:
                print(sql_state)
            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

insert2ReviewsTable()
insert2BusinessTable()
insert2Checkin()
insert2Review()