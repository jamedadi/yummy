Yummy
---
**This project is going to be a clone of sanpp food with Python and Django framework.**

---

## What is yummy?

It’s actually a service which users can order food very easily and restaurant managers can register their services so
that other people can use them.

As I said this is going to be a clone of this service , clearly It’s not going to implement all the features

---

## The goal of this project:

The main purpose of this project is being an acceptable resume and also a good practice of Django framework

---

## Features:

- [x] We will have two type of users in this project : 1 - Customer 2 - Service Provider.
- [x] Each service provider can provide different services such as (restaurant, fast food, confectionery, supermarket,
  …).
- [x] Each service will be able to have a menu containing different items.
- [x] Each service will be able to have custom categories for the items of the menu.
- [x] Each service provider must specify the supported areas for the item delivery for the service.
- [ ] Each service provider can add discount on some of their items for a limited time.
- [x] Each service will have active days and hours.
- [x] Each customer can have different addresses.
- [x] Each customer will be able to see the services(only the supported services in their area).
- [x] Each customer can add items to their cart(note : Each cart can only contain items from one specific service, that
  means adding items from different services causes multiple carts).
- [ ] Each customer will be able to add comment for the items which was in their cart after the order was delivered(
  note: customers will be able to add one comment for an item after each successful order).
- [ ] Each item will have a score based on its comments.
- [x] Each user will be to see the status of the order after the payment has been successful.
- [ ] The quantity of each item must be increased and decreased at successful orders.  

---

## Architecture of the project:

The project is based on the MVT architecture of the Django framework, so we will use SSR(server side rendering)

---
## How to run:

1- first create a virtualEnvirment
```
python3 -m venv .env
// or other ways to create a VENV
```
2- then activate it
```
source .env/bin/activate    
```
3- start to install requirments.txt file
```
pip install -r requirements.txt
```
note:
if suds-jurko throw error please install it in this way
```
pip install -i https://m.devpi.net/jaraco/dev suds-jurko    
```
then use 
```
pip install -r requirements.txt
```
4- on setting file you must change some places
  - you must set a DBMS and its settings(if you junior ad django use this [url](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)
  - you must set ```ALLOWED_HOSTS,DEBUG``` in setting file
5- start migrate to ctreate tables and columns in your choosen database
6- enjoy it :)



---
