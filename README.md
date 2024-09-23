# Customers API

A project to create customers and their Orders API endpoints.

## Project Goals
1. Create a simple Python o
2. Design a simple customers and orders database 
3. Add a REST API to input / upload customers and orders:
   - Customers have simple details e.g., name and code.
   - Orders have simple details e.g., item, amount, and time.
4. Implement authentication and authorization via OpenID Connect
5. When an order is added, send the customer an SMS alerting them (you can use the
Africa’s Talking SMS gateway and sandbox)
6. Write unit tests (with coverage checking) and set up CI + automated CD. You can deploy
to any PAAS/FAAS/IAAS of your choice
7. Write a README for the project and host it on your GitHub

# Technologies
 - Python Django
 - PostgreSQL
 - Django Rest framework
 - Nginx for reverse proxy
 - VPS for hosting

# Running / Deployment

- Run git clone `https://github.com/homemix/sales_API`
- Edit env_copy to match your settings
- Create virtual environment and run `pip install -r requirements.txt`
- Run the django project `python manage.py migrate`
- Run the django project `python manage.py collectstatic`
- Run the django project `python manage.py runserver 0.0.0.0:8000`
- Make sure it runs correctly and the initial django url is visible.

**The Project is also live at `http://51.210.142.16/redoc`**

# Endpoints
- All endpoints follow the REST FRAMEWORK architecture.
- Visit `http://51.210.142.16/swagger/` or `http://51.210.142.16/redoc/` for the complete list of Endpoints and testing.