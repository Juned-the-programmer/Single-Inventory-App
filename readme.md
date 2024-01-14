
## Pre-requisite

Need to setup cache server in local or Production sever to use a cache and celery automation tasks

* To setup on Linux

    - To Setup Cache Server

        - ` sudo dnf install memcached `

        #### NOTE : After Installing memched server cehck the status for it if it is running then fine or else start the service using

        - ` sudo systemctl start memcached `

        - ` sudo systemctl enable memcached `

        - ` sudo systemctl status memcached `
    
    - To setup celery

        - ` sudo dnf install python3-devel `

        - ` sudo dnf install redis `

## Setup Project

For setting up project clone it using URL

- ` git clone https://github.com/Juned-the-programmer/Single-Inventory-App.git `

Create a Virtualenv

- ` Virtualenv venv `

Activate Virtual env

- ` .venv/bin/activate `

Install Required packages using pip3

- ` pip3 install -r requirements.txt `

#### NOTE : Delete the current db.sqllite3 file to create a fresh database

Do Migrations 

- ` python3 manage.py makemigrations `

- ` python3 manage.py migrate `

And Run the Project using this command

- ` python3 manage.py runserver `

create a superuser 

- ` python3 manage.py createsuperuser ` 

provide valid username and password for your super user.

Visit the URL to create user for Estimate Account

- ` http://127.0.0.1:8000/auth/signup-estimate `

Now You can successfully login to the Application.

#### To start the celery task for now we have to di manually.

Run the following commands in the separate terminals.

- ` redis-server `

- ` celery -A Inventory worker --loglevel=debug `

- ` celery -A Inventory beat --loglevel=debug `


#### Feel Free to create any issue if it required for any suggestion. That will be appreciable
