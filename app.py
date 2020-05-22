from flask import Flask, redirect, url_for, render_template, session, request, g, send_from_directory,jsonify, flash
from actions import *
from queries import *
from datetime import date
import json

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/bla", methods=["GET", "POST"])
def bla():
    if request.method == "POST":
        return request.form["name"]
    return render_template("bla.html")



@app.route("/tiara")
def tiara():
    return render_template("Hotel.htm")

@app.route("/Details")
def details():
    hotels = select_all_hotels()
    return render_template("Details.html", hotels=hotels)

@app.route("/ReservationDetails")
def reservationdetails():
    hotels = select_all_hotels()
    if "user" in session:
        username = session["userid"]
        data = select_reservations_by_custid_res(username)
        return render_template("ReservationDetails.html", hotels=hotels, reservations=data)
    return render_template("Details.html", hotels=hotels)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/search", methods=["GET","POST"])
def search():
    hotel2s = select_all_hotels()
    if not 'resultLen' in session:
        session['resultLen'] = 0
    else:
        session.pop("resultLen", None)

    if request.method == "POST":
        hotelname = request.form["hotelname"]
        hoteltype = request.form["hoteltype"]
        cost = request.form["cost"]
        hotelid = hotel_id_from_name(hotelname)
        if cost == "<50":
            costmin = 0
            costmax = 50
        elif cost == "51-100":
            costmin = 51
            costmax = 100
        elif cost == "101-200":
            costmin = 101
            costmax = 200
        else:
            costmin = 201
            costmax = 1000000000000
        session['result'] = (search_hotel(hotelid, hoteltype, costmin, costmax))
        session['resultLen'] = len((session['result'])) + 10
        return render_template("home.html", hotels=hotel2s)
    return render_template("home.html", hotels=hotel2s)



@app.route("/AccountDetails")
def accountdetails():
    hotels = select_all_hotels()
    if "user" in session:
        username = session["user"]
        data = select_user_id_by_name_all(username)
        return render_template("AccountDetails.html", name=data, hotels=hotels)
    return render_template("login.html", hotels=hotels)


@app.route("/login", methods=["GET", "POST"])
def login():
    hotels = select_all_hotels()
    if "user" in session:
        return "user is currently logged in"
    if request.method == "POST":
        un = request.form["un"]
        pw = request.form["pw"]
        if user_in_db(un, pw):
            session["user"] = un
            session["userid"] = select_user_id_by_name(un)
            session["date"] = date.today()
            session["date_display"] = date.today().strftime("%D")
            return redirect(url_for("home"))
        else:
            error_login = True
            flash("username or password is incorrect")
        if un == "" or pw == "":
            flash("must provide all fields")
        
    return render_template("login.html", hotels=hotels, error_login=True)
    

@app.route("/logout")
def logout():
    hotels = select_all_hotels()
    session.pop("user", None)
    session.pop("userid", None)
    session.pop("date", None)
    session.pop("date_display", None)
    session.pop("admin", None)
    session.pop("hotelid", None)
    return render_template("home.html", hotels=hotels)


@app.route("/register", methods=["GET","POST"])
def register():
    error = False
    hotels = select_all_hotels()
    if request.method == "POST":
        fn = request.form["fn"]
        ln = request.form["ln"]
        un = request.form["un"]
        pw = request.form["pw"]
        if un == "" or pw == "" or fn == "" or ln == "":
            flash("must provide all fields")
            error=True
        if user_in_db(un):
            error=True
            flash("username already taken")
        if not error:
            insert_new_user(fn, ln, un, pw)
        return render_template("login.html", hotels=hotels, error=error)


#Loading Pages
@app.route("/")
def home():
    data = select_all_hotels()
    # session["date"] = "something"
    return render_template('home.html', hotels=data)


@app.route("/add_reservation", methods = ["GET", "POST"])
def add_reservation():
    data = select_all_hotels()
    if "user" in session:
        return render_template("reservations.html", hotels=data)
    return render_template("login.html",hotels=data) 

@app.route("/bookroom", methods=["GET","POST"])
def bookroom():
    data = select_all_hotels()
    if request.method == "POST":
        startdate = request.form["chckin"]
        enddate = request.form["chckout"]
        if "roomid" in session:
            if not check_reservation(startdate, enddate, session["roomid"]):
                custid = select_user_id_by_name(session["user"])
                resDetails = insert_new_reservation(startdate, enddate, session["roomid"], custid)
                session.pop("roomid", None)
                return render_template("confirm.html", d=resDetails, hotels=data)
    return render_template("reservations.html",hotels=data)

@app.route("/cancel_reservation", methods = ["GET", "POST"])
def cancel_reservation():
    data = select_all_hotels()
    if "user" in session:
        custid = select_user_id_by_name(session["user"])
        if "roomid" in session:
            if check_reservation_by_customer(custid, session["roomid"]):
                delete_reservation(custid, session["roomid"])
                session.pop("roomid", None)
                return render_template("ReservationDetails.html",hotels=data)
            return render_template("home.html",hotels=data)
        return render_template("login.html",hotels=data) 
    return render_template("login.html",hotels=data) 


@app.route("/reservations")
def reservations():
    hotels = select_all_hotels()
    if "user" in session:
        username = session["user"]
        data = select_reservations_by_custid(session["userid"])
        return render_template("reservations.html", d=data, hotels=hotels)
    return redirect(url_for("home"))


@app.route("/hotel/<chain>")
@app.route("/hotel/<chain>/<hotelname>", methods = ["GET", "POST"])
def hotel_page(chain, hotelname=None):
    data = select_all_hotels()
    if hotelname:
        for d in data:
            if chain == d[-1] and hotelname == d[2]:
                address = d[3:5]
                return render_template(
                    "hotel.html", 
                    name=hotelname, 
                    location=address, 
                    chain=chain,
                    hotels=data,
                    chain_id = d[0],
                    rooms = select_all_rooms_by_chain(d[0])
                )
        return redirect(url_for("home"), d=data)
    else:
        pass


@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = False
    hotels = select_all_hotels()
    if request.method == "GET":
        if "user" in session:
            flash("please logout first")
            error = True
            return render_template("admin_login.html", hotels=hotels, error_login=error)    
        elif "admin" in session: 
            return render_template("admin.html", hotels=hotels)
        else:
            return render_template("admin_login.html", hotels=hotels)
    elif request.method == "POST":
        un = request.form["un"]
        pw = request.form["pw"]
        if admin_in_db(un, pw):
            session["admin"] = un
            session["date"] = date.today()
            session["date_display"] = date.today().strftime("%D")
            session["hotelid"] = hotel_id_from_admin(un)
            return render_template("admin.html", hotels=hotels)
        else:
            error = True
            flash("Incorrect Login")
            if un == "" or pw == "":
                flash("All fields must be provided")
            return render_template("admin_login.html", hotels=hotels, error_login=error)
    return render_template("admin_login.html", hotels=hotels)

@app.route("/register_admin", methods=["GET","POST"])
def register_admin():
    hotels = select_all_hotels()
    error=False
    if request.method == "POST":
        hn = request.form["hn"]
        un = request.form["un"]
        pw = request.form["pw"]
        # insert_new_user(fn,ln,un,pw)
        if hotel_name_exists(hn):
            error=True
            flash("hotel already taken")
        if admin_in_db(un):
            error=True
            flash("username already taken")
        if un == "" or pw == "" or hn == "":
            flash("must provide all fields")
            error=True
        if not error:
            insert_new_hotel(hn)
            idn = hotel_id_from_name(hn)
            insert_new_admin(un,pw,idn)
            return render_template("admin.html", hotels=hotels)
        return render_template("admin_login.html", error=error, hotels=hotels)

@app.route("/admin_add_loc", methods=["GET","POST"])
def admin_add_loc():
    hotels = select_all_hotels()
    if request.method == "POST":
        name = request.form["name"]
        icord = request.form["iloc"]
        jcord = request.form["jloc"]
        cheapNum = request.form["cs"]
        cheapRate = request.form["cr"]
        expensiveNum = request.form["es"]
        expensiveRate = request.form["er"]
        # check that location isn't in use
        if not location_in_db(icord, jcord):
            # insert new location
            insert_new_location(session["hotelid"],name,icord,jcord)
            # grab new location id
            locid = get_locationid_from_cords(icord, jcord)
            # insert all cheap rooms
            x = 0
            while x < int(cheapNum):
                print("cheapTest")
                updated_insert_new_room(locid, "Cheap", cheapRate)
                x += 1
            # insert all expensive rooms
            x = 0
            while x < int(expensiveNum):
                print("exTest")
                updated_insert_new_room(locid, "Expensive", expensiveRate)
                x += 1

    return render_template("admin.html", hotels=hotels)


# Returning Data
@app.route("/getAllLocations")
def getAllLocations():
    return json.dumps(select_all_locations())

@app.route("/getAllCurrent")
def getAllCurrent():
    return json.dumps(current_reservations_by_admin(session["admin"], session["date"]))

@app.route("/getAllFuture")
def getAllFuture():
    return json.dumps(future_reservations_by_admin(session["admin"], session["date"]))
 
@app.route("/getAllReservations")
def getAllReservations():
    hotels = select_all_hotels()
    if "user" in session:
        custid = select_user_id_by_name(session["user"])
        return json.dumps(select_reservations_by_custid(custid))
    return render_template("login.html", hotels=hotels)

@app.route("/getAccountInfo")
def getAccountInfo():
    if "user" in session:
        custid = select_user_id_by_name(session["user"])
        return json.dumps(select_account_info(custid))

# Posting Data
@app.route("/add_room_to_session", methods=["GET","POST"])
def add_room_to_session():
    if request.method == "POST":
        session["roomid"] = request.form["roomid"]
        return session["roomid"]

# Test Routes
@app.route("/adam")
def adam():
    return render_template("confirm.html")



    
# @app.route("/login")
# def login_and_register():
#     return render_template("login.html")

# @app.route("/adminregistersubmit", methods=["POST"])
# def admin_registration():
#     pass


# @app.route("/home")
# def sendHome():
#     return render_template("bla.html")


# @app.route("/getData")
# def send_data():
#     data = [
#         (1, "Joseph"),
#         (2, "John")
#     ]
#     return json.dumps(data)

# @app.route('/postData', methods=["GET","POST"])
# def receivePost():
#     if request.method == "POST":
#         return json.dumps(request.form)

@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == "__main__":
    app.run(debug=True)