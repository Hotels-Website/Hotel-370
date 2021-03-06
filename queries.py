from contextlib import contextmanager
import sqlite3
import os

db = 'hotel.db'


# this turns the open and closing behavior into a "with statement" (less code)
# lookup context managers in python if curious 



@contextmanager
def create_connection(db):
    conn = sqlite3.connect(db)
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()

#CREATE
def create_db_and_tables():
    '''
    Hotel - id, name
    Location - id, hotel-id, name, i, j 
    Room - id, location-id, room-number, size, price, 
    CustomerAccount - id, first-name, last-name, DOB, username, password
    Reservation - id, start-date, end-date, room-id, cust-id
    Admin - id, username, password, hotel-id
    '''
    with create_connection(db) as c:
        c.execute("""
            CREATE TABLE if not exists hotel(
                id integer primary key,
                name text not null unique
            )
        """)

        c.execute("""
            CREATE TABLE if not exists location(
                id integer primary key,
                hotelid integer not null,
                name text not null,
                i integer not null,
                j integer not null,
                foreign key(hotelid) references hotel(id),
                unique(i,j),
                check(i >= 0 and i <= 100 and j >= 0 and j <= 100)
            )
        """)

        c.execute("""
            CREATE TABLE if not exists room(
                id integer primary key,
                locationid integer not null,
                type text not null,
                price real not null,
                foreign key(locationid) references location(id)
            )
        """)

        c.execute("""
            CREATE TABLE if not exists customer(
                id integer primary key,
                firstname text not null,
                lastname text not null,
                username text not null unique,
                password text not null
            )
        """)

        c.execute("""
            CREATE TABLE if not exists reservation(
                id integer primary key,
                startdate integer not null,
                enddate integer not null,
                roomid integer not null,
                custid integer not null,
                foreign key(roomid) references room(id),
                foreign key(custid) references customer(id)
            )
        """)

        c.execute("""
            CREATE TABLE if not exists admin(
                id integer primary key,
                username text not null,
                password text not null,
                hotelid integer not null,
                foreign key(hotelid) references hotel(id)
            )
        """)

#INSERT
def insert_new_user(firstname, lastname, username, password):
    with create_connection(db) as c:
        c.execute(f"insert into customer values (null,'{firstname}','{lastname}','{username}','{password}')")

    with create_connection(db) as c:
        c.execute(f"select * from customer where username='{username}'")
        data = c.fetchone()
    return data

def insert_new_hotel(hotel):
    with create_connection(db) as c:
        c.execute(f"insert into hotel (name) values ('{hotel}')")
        
    with create_connection(db) as c:
        c.execute(f"select * from hotel where name = '{hotel}'" )
        data = c.fetchone()
    return data



def insert_new_admin(username, password, hotelid):
    with create_connection(db) as c:
        c.execute(f"insert into admin (username, password, hotelid) values ('{username}','{password}',{hotelid})")

def insert_new_location(hotel, name, i,j):
    with create_connection(db) as c:
        c.execute(f"insert into location values (null,'{hotel}','{name}','{i}','{j}')")

    with create_connection(db) as c:
        c.execute(f"select id from location where name='{name}'")
        data = c.fetchone()
    return data

def updated_insert_new_room(locid, rt, price):
    with create_connection(db) as c:
        c.execute(f"insert into room (locationid,type,price) values ('{locid}','{rt}',{price})")



def insert_new_reservation(start, end, room, cust):
    with create_connection(db) as c:
        c.execute(f"insert into reservation (startdate, enddate, roomid, custid) values ('{start}','{end}','{room}','{cust}')")

    with create_connection(db) as c:
        c.execute(f"select * from reservation where startdate = '{start}' and custid = '{cust}'")
        data = c.fetchone()
    return data


#DELETE
def delete_reservation(custid, roomnum):
    with create_connection(db) as c:
        c.execute("""DELETE from reservation WHERE custid=? and roomid=?""", (custid, roomnum,))

#SELECT
def select_all_locations():
    with create_connection(db) as c: 
        c.execute(
            """select b.name, a.name, a.i, a.j
            from location as a
            join hotel as b
            on b.id = a.hotelid
            """)
        data = c.fetchall()
        print(data)
    return data

def check_reservation(startdate, enddate, room):
    with create_connection(db) as c:
        c.execute(
            f"""select roomid
            from reservation
            where reservation.roomid = '{room}'
            and reservation.startdate = '{startdate}'
            and reservation.enddate = '{enddate}'
            """)
        data = c.fetchone()
    return data

def check_reservation_by_customer(customer, room):
    with create_connection(db) as c:
        c.execute(
            f"""select roomid
            from reservation
            where reservation.roomid = '{room}'
            and reservation.custid = '{customer}'
            """)
        data = c.fetchone()
    return data

def select_unavailable_rooms(location):
    with create_connection(db) as c: 
        c.execute(
            """select room.id, room.type, room.price
            from room
            inner join reservation on room.id = reservation.roomid
            inner join location on location.id = room.locationid
            where location.name = '{location}'
            """)
        data = c.fetchall()
        print(data)
    return data

def location_in_db(i, j):
    with create_connection(db) as c:
        c.execute(
            f"""select i, j
            from location
            where location.i = '{i}'
            and location.j = '{j}' 
            """)
        data = c.fetchone()
    return data

def get_locationid_from_cords(i, j):
    with create_connection(db) as c:
        c.execute(
            f"""select id
            from location
            where location.i = '{i}'
            and location.j = '{j}'
            """)
        data = c.fetchone()
    return data[0]

def select_all_hotels():
    with create_connection(db) as c:
        c.execute(
            """select *
            from location
            join hotel
            on hotel.id = location.hotelid
            """)
        data = c.fetchall()
    return data

def select_all_rooms():
    with create_connection(db) as c:
        c.execute(
            """select *
            from room
            """)
        data = c.fetchall()
    return data

def select_all_available_rooms():
    with create_connection(db) as c:
        c.execute(
            """select room.id
            from room
            left join reservation on reservation.roomid = room.id
            where reservation.roomid IS NULL
            """)
        data = c.fetchall()
    return data

def select_all_rooms_by_chain(locid):
    with create_connection(db) as c:
        c.execute(
            f"""
            select room.id, room.locationid, room.type, room.price
            from location
            join hotel
            on hotel.id = location.hotelid
            join room
            on location.id = room.locationid
            where location.id = {locid}
            """)
        data = c.fetchall()
    return data

def select_all_available_rooms_by_chain(locid):
    with create_connection(db) as c:
        c.execute(
            f"""
            select room.id, room.locationid, room.type, room.price
            from location
            join hotel
            on hotel.id = location.hotelid
            join room
            on location.id = room.locationid
            left join reservation on reservation.roomid = room.id
            where location.id = {locid} and reservation.roomid IS NULL
            """)
        data = c.fetchall()
    return data

def select_user_id_by_name(name):
    with create_connection(db) as c:
        c.execute(
            f"""select id, username
            from customer
            where customer.username='{name}'
            """)
        data = c.fetchone()
    return data[0]

def select_user_id_by_name_all(name):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from customer
            where customer.username='{name}'
            """)
        data = c.fetchone()
    return data

def select_reservations_by_custid(id):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from reservation
            where reservation.custid={id}
            """)
        data = c.fetchall()
    return data

def select_reservations_by_custid_res(id):
    with create_connection(db) as c:
        c.execute(
            f"""select hotel.name,type,price,startdate,enddate,roomid
            from location
            join hotel
            on location.hotelid=hotel.id
            join room
            on room.locationid=location.id
            join  reservation
            on reservation.roomid=room.id
            where reservation.custid={id}
            """)
        data = c.fetchall()
    return data

def select_reservations_by_username(name):
    iden = select_user_id_by_name(name)
    select_reservations_by_custid(iden)

def select_account_info(custid):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from customer
            where customer.id = '{custid}'
            """)
        data = c.fetchone()
    return data


def user_in_db(un, pw=None):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from customer
            where customer.username = '{un}'
            {f"and customer.password = '{pw}'" if pw else ""}
            """)
        data = c.fetchone()
    return data
        
def admin_in_db(un, pw=None):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from admin
            where admin.username = '{un}'
            {f"and admin.password = '{pw}'" if pw else ""}
            """)
        data = c.fetchone()
        print(data)
    return data



def hotel_name_exists(name):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from hotel
            where hotel.name = '{name}'
            """)
        data = c.fetchall()
    return data
    
def hotel_id_from_name(name):
    with create_connection(db) as c:
        c.execute(
            f"""select id
            from hotel
            where hotel.name = '{name}'
            """)
        data = c.fetchone()
    return data[0]

def hotel_id_from_admin(name):
    with create_connection(db) as c:
        c.execute(
            f"""select hotel.id
            from hotel
            inner join admin on hotel.id = admin.hotelid
            where admin.username = '{name}'
            """)
        data = c.fetchone()
    return data[0]
    


def current_reservations_by_admin(admin, date):
    with create_connection(db) as c:
        c.execute(f"""
            select customer.firstname, customer.lastname, reservation.startdate, reservation.enddate, room.id
            from reservation
            inner join customer on customer.id = reservation.custid
            inner join room on reservation.roomid = room.id
            inner join location on room.locationid = location.id
            inner join admin on admin.hotelid = location.hotelid
            where admin.username = '{admin}' and reservation.enddate >= '{date}'
            """)
        data = c.fetchall()
    return data

def future_reservations_by_admin(admin, date):
    with create_connection(db) as c:
        c.execute(f"""
           select customer.firstname, customer.lastname, reservation.startdate, reservation.enddate, room.id
            from reservation
            inner join customer on customer.id = reservation.custid
            inner join room on reservation.roomid = room.id
            inner join location on room.locationid = location.id
            inner join admin on admin.hotelid = location.hotelid
            where admin.username = '{admin}' and reservation.startdate < '{date}'
            """)
        data = c.fetchall()
    return data


def drop_table(table):
    with create_connection(db) as c:
        c.execute(f"drop table if exists {table}")
        
def search_hotel(hotelid, hoteltype, costmin, costmax):
    with create_connection(db) as c:
        c.execute(f"""
        select room.id, location.name, room.type, room.price 
        from room
        join location
        on room.locationid = location.id
        join hotel
        on location.hotelid = hotel.id
        where hotel.id = '{hotelid}'
        and room.type = '{hoteltype}'
        and room.price >= '{costmin}'
        and room.price <= '{costmax}'
        """)
        data = c.fetchall()
    return data



import random
def initialize_dummy_data():
    firstnames = ["John", "Jacob", "Sean", "Adam", "Joseph"]
    lastnames = ["Smith", "Stevens", "Shah", "Schwartz"]
    hotel_names = ["Marriot", "Best Western", "Hilton"]
    location_name = ["New York", "San Francisco"]
    rooms = {"Cheap":50, "Expensive": 100}

    with open("login_credentials.txt", "w") as f:
        f.write("Customers\n")
        f.write("num: id fname lname username password \n\n")
        for i in range(20):
            fn = random.choice(firstnames)
            ln = random.choice(lastnames)
            cust_id, *_ = insert_new_user(fn, ln, fn+str(i), fn)
            f.write(f"{i}: {cust_id}, {fn}, {ln}, {fn+str(i)}, {fn}\n")
    
    i = 0
    for chain in hotel_names:
        cid, cname = insert_new_hotel(chain)
        insert_new_admin(chain, chain, cid)
        for location in location_name:
            i += 1
            # print(i)
            insert_new_location(cid, location, i, i)
            locid = get_locationid_from_cords(i,i)
            #print(locid)
            for room_type, room_price in rooms.items():
                for j in range(10):
                    updated_insert_new_room(locid, room_type, room_price)

    insert_new_reservation(5222020,5232020,1,1)
    insert_new_reservation(5222020,5232020,2,1)
    
def direct_test():
    #insert_new_reservation(5222020,5232020,0,0)
    #if check_reservation_by_customer(0,0):
    #   delete_reservation(0,0)

    custid = select_user_id_by_name("John0")
    print(custid)

def reset_db():
    os.remove("hotel.db")
    create_db_and_tables()
    initialize_dummy_data()


if __name__ == '__main__':
    reset_db()
    # direct_test()
