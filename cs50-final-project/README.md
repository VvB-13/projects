# MyFavorites!
#### Video Demo:  <https://youtu.be/0gG5YE3awpA>
#### Description:

Short Version:
MyFavorites is a flask web application where one can like movies, board games and computer games and have them displayed on their MyFavorites page. Plus there is an option to search for the favorites of other users.

The layout.html contains the main layout for all the html pages. It includes the head, navbar, message flashing and a main section which is different for each page as well as the title. The navbar displayes different content depending on weither the user is logged in or not.

The login.html and register.html pages handle the user managing process. The Register page contains a file which is generated with wtforms. One has to input a username, a password and confirm the password. The password have to be the same and the username must must not exist already. The user is flashed by a message (Pick a different username) if the username already exists. All of the other validation is handelt by the validators of wtforms. If the registration is successful the user is automatically put into the db (table user) and logged in. The login page is for logging in an existing user. Here the username and password is checked. If there is something wrong the user is flashed by a message (either password or username invalid).

The index.html displayes the favorites of the user in three different tables (board games, movies and computer games). If nothing is liked yet, the index page displays (Nothing liked yet). Through the displayed tables one can also directly delete a favorite. This deletes the entry in the db (table like).

The three pages board.html, movie.html and game.html display forms for the search for entries. The forms are created via wtforms. On every page there are two input fields to choose from, but one can also use both. For example searching for a movie by title and/or genre. After searching the result is displayed in a table limited to 10 entries. This is done by querying for matches in the db. There is a different table for movie, board game, and computer game. The displayed table also includes a like button. Via this button one can add entries to their favorites.

Then there is search.html, which allows the user to search for other users and their favorites. By searching for a user the favorites (board, movie, game) are displayed. But there is also the option to disallow this feature by going into setting.html (right side of the navabr) and toggling the radio button to "no". When one searches for a user, which does not want to share their favorites, a message is displayed (User does not exist or does not want to share). Then there is also a button to logout on th right corner of the navbar, which does exactly that.

The whole side is kept quite minimalistic. The css for the forms, tables and navbar are from bootstrap. The background is colorful but not to heavy on the eyes. The content is centered.

The forms for the searches and login managent are created in a different python file called self_forms.py. These forms are later imported to the main file.

The main python file is called app.py. It sets up the application with flask. Also flask login, sqlalchemy, encrypt and automap is used. With flask login is the whole login managament handled. The Login manager is setup and the User class is created, which later creates a table inside the db. For this sqlite3 is used. Through the register form a user is created inside the db (with an id, username, password). The id is used to loggin the user. Flask login tracks if the user is loged in or not, thus enabling us to require login for flask routes. Via the route register the form data is validated and used to create a user. The login route checks the validity of the login form and logs the user in. The logout route is used to logout the user.

The board, movie and game route each handle the pages and db for the respective search. First the form is passed into the page when accessed via get. If the form is submit the input is validated and the result is displayed by querying for the right db entries. If a user likes one of the results it is passed into the like table of the db by attaching the entry_id into the submit button or precisly into a hidden input tag. The liking is handled by a if method equal post statement.

The setting route handles the form for changing share settings. And queryes the db. The boolean column for this is part of the user db. There are three tables, which are just for select querys (board, game and movie). And two tables for reading and writing data user and like.

For search and index the three different "favorites" board games, movies and computer games are passed into the respective template in order to display the favorites of oneselfs or another user.

Automap is used to access the existing classes and the tables of the db. Becrypt is used to hash the password of a user when registering and unhash it for validation when logging in. All of the querying is done by sqlalchemy.

