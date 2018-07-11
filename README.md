# PokeFlask 0.1
This web app is a project for the Udacity Full Stack Web Developer Nanodegree.

## About
This project is a RESTful web application utilizing Python with the Flask web framework connected with a SQL database to store Pokemon and its respective Pokemon types. Google Oauth2 is used to authenticate users, then they can add, edit and delete their own Pokemon and Pokemon Types. The user can only edit or delete the items created by him.

## In This Repo
This project has one main Python module `app.py` which runs the Flask application. A SQL database is created using the `database_setup.py` module and you can populate the PokeFlask with some Pokemon using `database_init.py`.
The Flask application uses stored HTML templates in the templates folder. PokeFlask also uses CSS (can be found in the static files) and Bootstrap 4.0 (CSS and JS imported from its CDN in base.html)

## Installation
1. Install Vagrant (https://www.vagrantup.com/)
2. Install VirtualBox (https://www.virtualbox.org/wiki/Downloads)
3. Windows users --> Download Git Bash (https://gitforwindows.org/)
4. Clone the Udacity Vagrantfile (https://github.com/udacity/fullstack-nanodegree-vm)
5. Go to /vagrant directory on the Git Bash terminal and either clone this repo or download and place zip
6. Launch the Vagrant VM ($ vagrant up) - it's all setup to run the application
7. Log into Vagrant VM ($ vagrant ssh)
8. Navigate to ($ cd/vagrant) as instructed in terminal
9. Setup application database ($ python /item-catalog/database_setup.py)
9. Insert some Pokemon  ($ python /item-catalog/database_init.py)
9. Run application using ($ python /item-catalog/app.py)
10. Access the application locally: http://localhost:5000

## Using Google Login
To get the Google login working there are a few additional steps:
It's important to accomplish those steps if you want the maximum experience from PokeFlask 0.1

1. Go to Google Developers(https://console.developers.google.com)
2. Sign up or Login with your account
3. Go to Credentials to create your own client ID
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'item-catalog'
7. Authorized JavaScript origins = 'http://localhost:5000'
8. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in templates/login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in item-catalog directory that you cloned
14. Run application ($ python /item-catalog/app.py)

## Future Versions will have
1. Responsive layout for phone and tablet screen sizes (The version 0.1 is optimized only for desktop screens)
2. A search bar to find Pokemons by name, type or user (creator)

## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/JSON`
    - Displays the whole catalog. Categories and all items.

Categories JSON: `/catalog/categories/JSON`
    - Displays all categories

Category Items JSON: `/catalog/<path:category_name>/items/JSON`
    - Displays items for a specific category

Category Item JSON: `/catalog/<path:category_name>/<path:item_name>/JSON`
    - Displays a specific category item.

## Accessing the DB
1. Open another terminal window and go to the Vagrantfile directory
2. Log into Vagrant if you're already logged in ($ vagrant ssh)
3. Go to the PokeFlask directory again
4. Run ($ sqlite3) in the terminal to access SQLite
5. Run (sqlite> .open "itemcatalog.db") to access the database
6. Launch (sqlite> .tables) to check the tables on the database (item, category and user)
7. To check all the Pokemon (sqlite> select * from item)
8. To check all the Pokemon Types (sqlite> select * from category)
9. To check all the users (sqlite select * from user)

## Considerations
This application can be used for another purposes instead of Pokemon. The py and db files are generic named with item and category. I hope you enjoy it!
