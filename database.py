import sqlite3
from datetime import date
#
# dATABASE SPEC
# drivers table list of phoneNum (BIGINT-integer), location(string)
DATABASE = "data.sqlite"
def createDatabase(file: str):
    """
    Limited to one delivery per day right now, but can change to date to increasee to more
    """
    # open a SQLite connection
    # a database file called data.db will be created,
    # if it does not exist
    con = sqlite3.connect(file)

    # create the database table if it doesn't exist
    delivery_schema = """
    CREATE TABLE IF NOT EXISTS delivery (
        driverNum BIGINT,
        weight SMALLINT,
        date DATETIME,
        location TEXT,
        confirmed BOOL NOT NULL
        PRIMARY KEY (date, driverNum)
    );
    """
    farmer_schema = """
    CREATE TABLE IF NOT EXISTS farmers(
        farmerNum BIGINT,
        weight SMALLINT,
        date DATE,
        driverNum BIGINT,
        location TEXT,
        confirmed BOOL NOT NULL
        PRIMARY KEY (date, driverNum, farmerNum)
    );
    """
    #Each person is create as an object. 
    people_schema = """
    CREATE TABLE IF NOT EXISTS people(
        phoneNum BIGINT,
        activity SMALLINT,
        status SMALLINT,
        PRIMARY KEY (phoneNum)
    );
    """

    with con:
        con.execute(farmer_schema)
        con.execute(delivery_schema)
        con.execute(people_schema)
        con.execute(people_schema)
        # con.execute(driver_schema)

def addData(file: str, type: str, date: date, weight: int, phoneNum: int, location: str, driverNum: int = 0):
    """
    Keyword arguments:
    type - "driver" or "farmer" (anything else will work as long as not driver)
    date - python date object, needs day, month, year - date of delivery
    weight - weight able to carry or weight requested
    location - str to be sent to driver or farmers to help choose driver
    driverNum - only for farmers (the driver taking their weight on that day)
    """
    con = sqlite3.connect(file)
    with con:
        if (type.lower() == "driver"):
            insert_query = """INSERT INTO delivery (driverNum, weight, date, location)
            VALUES (?, ?, ?, ?);
            """
            con.execute(insert_query, (phoneNum, weight, date.isoformat(), location))
            # Return true if worked
            return True
        
        else:
            insert_query = """
            INSERT INTO farmers(farmerNum, weight, date, location, driverNum)
            VALUES (?, ?, ?, ?, ?);
            """
            con.execute(insert_query, (phoneNum, weight, date.isoformat(), location, driverNum))
            return True

def get_deliveries(date: date, weight: int = 1):
    """
    Returns an array of driverPhone, location etc.
    """
    # For every available driver
        
    # Find out how much capacity they have left
    # Return drivers with capacity >= capacity demanded
    getDrivers = """
    SELECT
    delivery.driverNum,
    delivery.weight - IFNULL(SUM(farmers.weight), 0) AS capacity,
    delivery.location AS location
    FROM
        delivery
    LEFT JOIN
        farmers ON delivery.driverNum = farmers.driverNum AND delivery.date = farmers.date
    WHERE
        delivery.date = ? 
    GROUP BY
        delivery.driverNum, delivery.weight
    HAVING
        capacity >= ?;
    """
    con = sqlite3.connect(DATABASE)
    with con:
        result = con.execute(getDrivers, (date.isoformat(), weight))
        #Field names plus rows
        return ([i[0] for i in result.description], result.fetchall())

def set_activity(phone_num, new_activity: int = 0, state: int = 0) -> int:
    """
    Defaults state to 0
    """
    con = sqlite3.connect(DATABASE)
    with con:
        insert_query = """
            INSERT INTO people(phoneNum, activity, status)
            VALUES (?, ?, ?);
            """
        con.execute(insert_query, (phone_num, new_activity, state))
        return new_activity
    
def update_activity(phone_num, new_activity: int) -> int:
    con = sqlite3.connect(DATABASE)
    with con:
        update_query = """
            UPDATE people
            SET activity = ?
            WHERE phoneNum = ?;
        """
        con.execute(update_query, (new_activity, phone_num))
        return new_activity

def update_status(phone_num, new_status: int) -> int:
    con = sqlite3.connect(DATABASE)
    with con:
        update_query = """
            UPDATE people
            SET status = ?
            WHERE phoneNum = ?;
        """
        con.execute(update_query, (new_status, phone_num))
        return new_status
    

def get_person(phone_num: int) -> list[int, int]:
    con = sqlite3.connect(DATABASE)
    with con:
        res = con.execute(f'SELECT * FROM people WHERE phoneNum = {phone_num}').fetchall()
        if (len(res) == 0):
            return [None, None]
        else:
            print(res)
            return res[0][1], res[0][2]
        
def update_delivery_date(phone_num: int, delivery_date: date):
    """
    Updates it so can be refrenced when confirming delivery_date
    """
    con = sqlite3.connect(DATABASE)
    with con:
        update_query = """
            UPDATE people
            SET posDriverNum = ?
            WHERE phoneNum = ?;
        """
        con.execute(update_query, (delivery_date, phone_num))
        return new_status


def getTable(file: str, tName: str):
    """
    Returns string of tName table with all records
    """
    con = sqlite3.connect(file)
    with con: 
        res = con.execute(f'SELECT * FROM {tName};')
        return res.fetchall()

if __name__ == "__main__":
    import os
    # Initial data
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    createDatabase(DATABASE)
    addData(DATABASE, "driver", date.today(), 200, 7752715719, "Street 15")
    addData(DATABASE, "driver", date.today(), 200, 8890123412, "Street 16")
    addData(DATABASE, "farmer", date.today(), 50, 123456789, "Street 2", 7752715719)
    
    print(getTable(DATABASE, "farmers"))
    print(get_deliveries(DATABASE, date.today(), 20))



#
# Querying the database
#

# query the database for ALL data in the notes table
# cur.execute('SELECT * FROM notes;')

# # print the result
# result = cur.fetchall()
# print(result)

# #
# # Cleaning up
# #

# # close the cursor
# cur.close()

# # close the connection
# connection.close()


