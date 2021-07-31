# What are people saying about.

Code for: https://whatarepeoplesayingabout.com
- Status: offline, not yet deployed...

&nbsp;

Aim: Project that let's people have their say on whatever topic they so choose.

## Django basics
- python manage.py runserver

### Create an app
python manage.py startapp APPNAME

### Create migrations
python manage.py makemigrations

### Run migration
python manage.py migrate

### Collect Static Files
python manage.py collectstatic


## How it's built.
- **Server**: The main server used for server side rendering and core business logic of course is django.
- **Client**: The django templating language mixed with JS and CSS files. We are also leaning heavily on
the hyperbox.js file to build reactive layouts. notice the `x()` functions all within the scripts.

### The apps
The `WhatArePeopleSayingAbout` ap contains the main settings.
- `app` contains mainly common implementations. It also contains ALL CSS and JS.
- `api` contains all api url definitions and specifies common API functionality.
- `app_auth` contains the custom authentication and the main `User` model.
- `interactions` contains all interaction logic e.g. anything surrounding posts, comments and likes.
Interactions has individiual sub modules for each entity (post/comment/topic/likes). Inside these sub modules we
have the following:
    - `/api` contains the main api views for the submodule.
    - `/services` contains re-useable business logic for the sub module.
    - `Root level files` standard django app stuff like serialzers and models.


# Deployment
The `settings.py` file contains the main production settings while `settings_dev.py`
contains the dev settings that override settings.py. 

- `settings.py` essentialy acts as out base settings which are prod.

Run using normal docker file:  
`docker-compose up --build`
Run using the prod file:
- `docker-compose -f docker-compose-deploy.yml up --build -d`

deploy: https://www.youtube.com/watch?v=IoxHUrbiqUo

connecting to ec2 instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html

- `docker container exec -it 08aa40084067 python manage.py migrate`
- `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' whatpeoplearesayingabout_db_1`