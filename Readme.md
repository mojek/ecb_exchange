# ECB exchange  
Fetching exchange rate from  EU Central Bank via RSS.


## Installation:

**Clone repository:**  
git clone git@github.com:mojek/ecb_exchange.git

**Build the project with docker:**  
make build (or docker-compose exec web docker-compose up --build)

**Open new terminal and fire migrations:**  
make migrate (or docker-compose exec web python manage.py migrate)

**Create superuser:**  
make createsuperuser (or docker-compose exec web python manage.py createsuperuser)

**Log in**  
Open http://localhost:8000/api/v1/currencies/   
Click the upper right corner log in and log in with your superuser.

**Add some currencies:**  
name: US dollar  
short_name: USD  
rss_link: https://www.ecb.europa.eu/rss/fxref-usd.html  

In currency API there is an exchange URL, click and see exchanges scraped from ECB.


## Data models

**Currency:**  
name: string  
short_name: string(3)  
rss_url: url(200)  
last_fetch: date *# a date of the last fetched exchange*

**Exchange**  
currency: currency  
exchange_date: date  
rate: decimal  

The fetcher make his job after the creation of currency via Api (when you do it via admin panel nothing will happen). The job is sending to Celery worker.  
There is also Celery beat that downloads data every day at 3 p.m.
