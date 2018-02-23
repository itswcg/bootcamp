# Bootcamp2  
#### Bootcamp2 is my-built wheel based on [bootcamp](https://github.com/qulc/bootcamp) with [Django 2](https://github.com/django/django).   
![](https://github.com/itswcg/bootcamp2/blob/master/bootcamp2/static/img/pic1.png)
![](https://github.com/itswcg/bootcamp2/blob/master/bootcamp2/static/img/pic2.png)  

## Some new features  
* Django 2 and Python 3.6
* [Follow system](https://itswcg.com/2018-01/bootcamp2.html)   
* Direct messages button  
* Home page optimization  
* Aticle and question relate to feed  

## Demo  
Please visit:  

* Deploy to heroku: <https://bootcamp2.herokuapp.com/>

## Install Guide
```bash
$ git clone https://github.com/itswcg/bootcamp2.git
$ cd bootcamp2/

# Use Python 3.6 virtualenv or pyenv
$ python -m venv venv 
$ source venv/bin/activate
$ python -m pip install -r requirements.txt

# Add DATABASE_URL, REDIS_URL config to env
$ export REDIS_URL=redis://localhost:6379/0
$ export DATABASE_URL=postgres://postgres:@localhost:5432/bootcamp2

# Cloudinary image setting
# please fill in api_key and api_secret in bootcamp2/bootcamp2/core/views.py

# Setting
# bootcamp2/settings.py DEBUG = True

# Create Tables
$ python manage.py makemigrations
$ python manage.py migrate

# Test
$ python manage.py test

# Run
$ python manage.py compilemessages #可省略
$ python manage.py collectstatic
$ python manage.py runserver
```


