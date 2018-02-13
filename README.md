# Item Catalog Project

### About this Project:

The Item Catalog Project is one of the harder projects I've done in my Udacity courses. It was a challenge to put together this web application, but I think it was really helpful! This project was intended to practice my understanding of CRUD operations, and implement them in a functioning web application. I based my item catalog on the video game [Katamari Damacy](https://en.wikipedia.org/wiki/Katamari_Damacy), which has its own extensive item catalog. All the writing for the catalog entries comes from this game.

### Requirements:
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- Python

### Components of this Project:
- `database_setup.py`, which creates the database
- `lotsofitems.py`, which can be run to pre-populate the database with some information
- `application.py`, which is the application itself
- The `static` folder, which contains the CSS document
- The `templates` folder, which contains all the HTML documents

### How To Run:

- Download the project [here](https://github.com/Genevieve-Wollner/catalog_project) and make sure you have Vagrant and VirtualBox installed. Place the `catalog` folder from the project in the `vagrant` folder for the virtual machine.
- Launch the virtual machine by typing `vagrant up` in the `vagrant` directory, followed by `vagrant ssh`.
- Once connected, type `python database_setup.py` to set up the database, you can run `python lotsofitems.py` at this time as well if you want to pre-populate the database with some items.
- Run `application.py` by typing `python application.py`, this will run the application on [http://localhost:8000](http://localhost:8000)
- Open your favorite browser to the above URL and log into the application with your Gmail account. The catalog can still be viewed without logging in.
- Freely browse the items catalogue!
