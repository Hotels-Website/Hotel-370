# How to get set up:
1. download the following if you don't already have it:
  - ```python3```, this will install ```pip``` (python package manager) as well
  - git
2. once git is installed you can, from the command line (```cmd``` on windows, ```terminal``` on mac), cd into your preferred location and run ```git clone https://github.com/Hotels-Website/Hotel-370.git``` to download this repository into that folder.
3. run ```pip install -r requirements.txt``` to install the dependencies
4. to run the app, cd into the just cloned repository and type ```python app.py```
5. if you run into an error such as ```ModuleNotFoundError: No module named 'flask'``` or something similar, run "pip install flask" or whichever module was mentioned, to install the required library
6. When the app is successfully running, a local server is started.  You should see this...

```
(hotelRes) C:\Users\Joseph\Desktop\HotelRes>python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 841-872-074
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

7. type http://127.0.0.1:5000/ into your address bar to see the website on your local computer
8. flask has live reloading, so as you save changes the server reloads automatically.
9. bootstrap and jquery are already imported - you don't need to use either but you can.

--------------------------------------------------
the important files to look at are app.py, queries.py and templates/

# Technologies
1. git - version control - how we can all work together and not step on each others toes
2. flask - web framework (handles server routes and sessions, etc.) - https://flask.palletsprojects.com/en/1.1.x/quickstart/
3. sqlite3 - simple db that stores in a single file
4. bootstrap (css framework) - https://getbootstrap.com/docs/4.4/getting-started/introduction/ - makes css way easier to use imho.
5. html, css, javascript
6. jinja - if you see code that looks like ```{% something %}``` in the html files, this is jinja.  it's used by flask to pass data to the html files before they get rendered. 
7. XMLHttpRequest - A way of sending asyncronous http requests from javascript
8. python Decorators - you will see ```@something``` above some functions in the python code - https://book.pythontips.com/en/latest/decorators.html - these essentially wrap the following function with some other code. They "decorate" the function, so to speak.  

```
def my-decorator(func):
  def decorated_function():
    print("some code before")
    func()
    print("some code after")
  return decorated_function
  
  
@my-decorator
def hello_world():
  print("hello world")
  
>>> hello_world()
Some code before
hello world
some code after

```

The live website is here https://protected-falls-95338.herokuapp.com/

------------------------------------------------------------------------

# HotelRes
Hotel Reservation App - CS370 Project 2b

Map
Customers
Hotels
Search Engine
Current Date

# Map
Don't need password to view map
Map - 0-100 grid, Location (i, j)

# Reservation Search Engine - Customer view
Search by
- Hotel
- Room size
- Price 
- Location

# My Reservations

# Customer Account
- login
- register

# Hotel Page
- Rooms - type
- rates
- availability

# Hotel Admin Account
- locations
- Add new location
- Who's checked in to which rooms

# Current date


import sqlite3

def create_db_and_tables():
    sqlite3.connect('game.db')
    c.execute("""

    
    
    """)










import sqlite3
from pprint import pprint

def getData():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()

    # c.execute(""" CREATE TABLE players
    # (
    #     username text,
    #     password text,
    #     email text,
    #     highscore real
    # )
    # """)

    # c.execute("INSERT INTO players VALUES ('SSM','pass','iun@iun.com','78343.43')")

    c.execute('select * from players')
    # data = []
    # for username, password, email, highscore in c.fetchall():
    #     data.append({
    #         "username":username,
    #         "password":password,
    #         "email":email,
    #         "highscore":highscore
    #     })
    data = "||".join(["::".join((un, pw, str(hs))) for un, pw, email, hs in c.fetchall()])
    print(data)
    conn.commit()
    conn.close()
    return data

def insert(data):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO players VALUES {data}")
    conn.commit()
    conn.close()

def scores():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('select distinct username, highscore from players order by highscore desc')
    data = "||".join(["::".join((a, str(b))) for a,b in c.fetchall()])
    print(data)
    conn.commit()
    conn.close()
    return data


def update(username, score):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute(f"select distinct highscore from players where username = '{username}' ")
    if c.fetchone()[0] < float(score):
        # print(c.fetchone()[0] < score)
        c.execute(f"UPDATE players SET highscore = {score} WHERE username = '{username}'")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    getData()
    scores()
    update("JSM", 118)


#git commands

mkdir
cd
cls
git init //you souldnt need this
git status
git add
git branch // to view branches
git checkout -b [newbranchname] // create and enter new branch





- step1 - download git and install

- step4 - in terminal or command prompt or git bash
- - go to folder (cd) you want to host the folder within 
- step5 - "git clone https://github.com/Hotels-Website/Hotel-370.git"
- step6 - create a new branch for yourself - "git checkout -b your_actual_name"
- step7 - create a new file in the folder called your_actual_name.txt but write your actual name
- = "git add your_actual_name.txt" or "git add ." then git commit -m "Initial Commit" 
- step8 - git push
- step9 - if your branch doesn't exist on github, you will be prompted to type
-         git push --set-upstream origin "your_actual_name"



#the production cycle
- after you've completed the aboce steps
- from then on 
- 1 - git pull origin master - get all the latest changes
- 2 - make changes to files yourself
- 3 - see changes you've made - git diff
- 4 - see files you've modified - git status
- 5 - add the changes - git add filename or git add .
- 6 - create a commit for all those changes - git commit -m "description of changes"
- 7 - git push


# What's left
1. inform if "location already exists" on admin
2. make sure location is 0 < i and j  < 100 
2. book and cancel reservations on search page
3. book and cancel reservations on hotel page
4. Display if certain room type is sold out
5. if not logged in customer prompted to login when attempts to make any reservation
6. inform customer when name is already taken
7. data validation - no fields should be blank or improperly formatted 
7. dollars signs next to prices
8. search - input selection criteria we think are relevant
9. sort query by room rates or hotel names
10. display count of all search results
11. input date when accessing the website for the first time, reprompted upon subsequent login
12. report 
- names 
- how to access and run
- admin account credentials
- screenshots with explanations of our work
1. Format of team meetings (online?), e.g. videoconference? email? Facebook? etc.
2. Summary/schematic of the project architecture.
3. Assignment of project responsibilities to team members, i.e. what did each person do.
4. A list of the project goals/milestones.
5. A timeline of progess for the completion of the project milestones.
6. A list of unit tests and a timetable when each test was successfully passed.
7. If necessary, what corrective steps were taken if the work fell behind schedule



What should we add?
we should have an initialize 1 non-admin user with a booked page
so we can see if reservations works


