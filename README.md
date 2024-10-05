# Django E-commerce Platform

This is a simple e-commerce platform built with **Django** and **Django REST Framework**. The project includes basic functionalities such as product listing, shopping cart, user authentication, and a basic order system. I also implemented background tasks using **Celery** for sending emails.
Integrated a simple payment flow.

## Features

- **Product Management**: Users can view products and paginate through them.
- **Shopping Cart**: Users can add items to their cart, adjust quantities, and view cart totals.
- **User Authentication**: Users can register, log in, and manage their profiles.
- **REST API**: The project provides endpoints for user authentication, products, cart management, and orders.
- **Caching**: Redis is used to cache the first few pages of products for faster loading.
- **Background Tasks**: Celery is used with Redis to send emails (notifications) in the background.
- **Basic Payment Flow**: A conceptual payment system is implemented to show how users can proceed to checkout and simulate payments using stripe.

## Setup Instructions

This project is containerized using **Docker** and **Docker Compose**. Follow these steps to set up the development environment.

### Prerequisites

- Docker
- Docker Compose

### Steps to Run the Project

1. **Clone the Repository**:

   ```
   From the root folder run the following commands
   ```

2. **Build and Run the Docker Containers**:
   Run the following command to build the images and start the services:

   ```bash
   docker-compose up --build
   ```

   This command will set up the following services:

   - **Django App (web)**: Runs the Django server.
   - **PostgreSQL (db)**: Database used to store user and product data.
   - **Redis**: Used for caching and as the result backend for Celery tasks.
   - **Celery Worker**: Handles background tasks (e.g., sending emails).

3. **Run Database Migrations**:
   After the containers are up, you need to apply the migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a Superuser**:
   You can create a superuser to access the admin panel:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the Application**:

   - Web: [http://localhost:8000](http://localhost:8000)

6. **Run Celery Worker** (in another terminal):

   ```bash
   docker-compose exec celery celery -A ecommerce worker --loglevel=info
   ```

7. **Run Tests**:
   To run the test suite, use:
   ```bash
   docker-compose exec web python manage.py test
   ```

### Docker Commands

- **Build and start the containers**: `docker-compose up --build`
- **Stop the containers**: `docker-compose down`
- **Run Django commands**: `docker-compose exec web python manage.py <command>`
- **View Celery logs**: `docker-compose logs celery`

## Features Breakdown

### 1. **Notification System**

- I implemented a simple notification system where emails are sent to users using Celery as a background task.
- Emails are sent using Django's email framework (`send_mail`) and processed by Celery to avoid blocking the main thread.
- **Limitation**: This system uses a local email backend, so it is not suitable for production. In production, you would need to integrate with a real email service (e.g., SMTP, SendGrid).

### 2. **Payment System**

- A very basic conceptual payment flow is implemented where users can proceed to checkout, simulate payments, and complete orders.
- **Limitation**: This is not a real payment gateway integration. For production, you'd need to use services like Stripe or PayPal.

## Limitations

1. **Email Notifications**:
   - The email notification system is not production-ready. It uses Django's default email backend, which needs to be replaced by a real email service (e.g., SMTP, Mailgun) in a production environment.
2. **Payment System**:
   - The payment system is conceptual and not integrated with any real payment gateways. For real-world usage, this part should be replaced by integrations with services like Stripe, PayPal, etc.
3. **Security**:
   - The project is not fully secured for production (e.g., it does not enforce HTTPS, and security settings like `ALLOWED_HOSTS` and `SECURE_SSL_REDIRECT` are not configured).
4. **Performance**:
   - Although I use Redis caching, the current setup caches only the first five pages of product listings for one hour. More sophisticated caching strategies and optimization techniques would be required for a large-scale application.
5. **Scalability**:
   - This project is not designed to scale for a high-traffic environment. Features like load balancing, database replication, and horizontal scaling are not set up.
6. **ENV**:
   - Didn't use values in .env file. As it not production ready code. Didn't think about it.

## Future Improvements

- **Real Payment Gateway**: Integrating a real payment provider like Stripe.
- **Production Email System**: Switching to a production email backend (e.g., SendGrid).
- **Complete Testing**: Write more comprehensive tests, including integration and unit tests for all endpoints.
- **Advanced Caching**: Add caching for other parts of the site and implement cache invalidation strategies.
