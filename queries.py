from contextlib import contextmanager
import sqlite3

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


def insert_new_hotel(hotel):
    with create_connection(db) as c:
        c.execute(f"insert into hotel (name) values ('{hotel}')")


def insert_new_admin(username, password, hotelid):
    with create_connection(db) as c:
        c.execute(f"insert into admin (username, password, hotelid) values ('{username}','{password}',{hotelid})")


def insert_new_location(hotel, name, i,j):
    with create_connection(db) as c:
        c.execute(f"insert into location values (null,'{hotel}','{name}','{i}','{j}')")


def insert_new_rooms(rooms):
    with create_connection(db) as c:
        for locid, rn, size, price in rooms:
            c.execute(f"insert into room (locationid,roomnumber,size,price) values ({locid},{rn},{size},{price})")

def updated_insert_new_room(locid, rt, price):
    with create_connection(db) as c:
        c.execute(f"insert into room values (null, '{locid}','{rt}','{price}')")


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

def select_user_id_by_name(name):
    with create_connection(db) as c:
        c.execute(
            f"""select id, username
            from customer
            where customer.username='{name}'
            """)
        data = c.fetchone()
    return data[0]

def select_reservations_by_custid(id):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from reservation
            where reservation.custid={id}
            """)
        data = c.fetchall()
    return data

def select_reservations_by_username(name):
    iden = select_user_id_by_name(name)
    select_reservations_by_custid(iden)



def user_in_db(un, pw):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from customer
            where customer.username = '{un}'
            and customer.password = '{pw}'
            """)
        data = c.fetchone()
    return data
        
def admin_in_db(un, pw):
    with create_connection(db) as c:
        c.execute(
            f"""select *
            from admin
            where admin.username = '{un}'
            and admin.password = '{pw}'
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
    

def select_rooms_search_criteria():
    pass

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

def initialize_dummy_data():
    hotelid = 0
    hotel, location = "Hilton", "New York"
    i, j = 20, 15
    hotel2, location2 = "Hilton", "San Francisco"
    i2, j2 = 2, 11
    with create_connection(db) as c:
        c.execute(f"insert into hotel(name) values ('{hotel}')")
    with create_connection(db) as c:
        c.execute(f"insert into location(hotelid, name, i,j) values ('{hotelid}','{location}','{i}','{j}')")
    with create_connection(db) as c:
        c.execute(f"insert into location(hotelid, name, i,j) values ('{hotelid}','{location2}','{i2}','{j2}')")


if __name__ == '__main__':
    # create_db_and_tables()
    # initialize_dummy_data()
    # print(select_all_hotels())
    # print(select_reservations_by_custid(select_user_id_by_name("blabla")))
    # insert_new_rooms(
    #     [(1, 1, 50, 200)]
    # )
    # print(select_all_hotels())
    # print(select_all_locations())
    # print(select_all_rooms())
    # print(select_all_rooms_by_chain(1))
    create_db_and_tables()