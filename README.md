# BubuKappa

BubuKappa is a web-based bookstore training project built with Django. The project implements a core e-commerce platform designed for selling books, manga, and related publications.

---

## Key Features

The following features have been successfully implemented in the project:

### 1. Catalog & Product Management
* Structured models for Categories, Products, and ProductImages.
* Optimized queries using `select_related` and `prefetch_related` to resolve N+1 query issues.
* Django Admin panel configuration featuring custom filters and inline model editing.
* Advanced product filtering and sorting capabilities.

### 2. User Accounts & Profiles
* Customized authentication via `CustomUser` and `UserProfile` models.
* Automated profile creation and updates using Django Signals.
* User profile page displaying account details and order history.

### 3. Shopping Cart System
* Dual-layered cart mechanics: hybrid session-based and database-backed shopping cart.
* Seamless synchronization and merging of the session cart into the database cart upon user authentication.
* Dynamic cart updates utilizing AJAX requests.
* Integrated context processor for global cart access across templates.

### 4. Search Mechanisms
* Advanced product search functionality utilizing Django `Q` objects.
* Live search with autocomplete capabilities: AJAX endpoint combined with Vanilla JavaScript to display matches in a dropdown under the input field, including text highlighting.

### 5. Checkout & Order Processing
* Order management system including `Order`, `OrderItem`, and `ShippingAddress` models.
* Dynamic multi-step checkout process with a transactional order creation pipeline that correctly handles inventory reduction (`stock`).
* Detailed order status history tracing (`OrderStatusHistory`).
* Advanced order status system containing timeline visualizations and structured status states (`pending`, `processing`, `shipped`, `delivered`, `cancelled`).
* Order cancellation option restricted to a 24-hour window from the creation time, including estimated delivery date calculations.
* Automated HTML email notifications sent upon successful order creation.

### 6. User Behavior Tracking
* Recently viewed items feature tracking up to 10 products using session and cookie storage, rendered via a dedicated context processor.

### 7. Optimization, Security & Architecture
* Integrated Django messages framework for user feedback notifications.
* Basic test coverage for critical application components including models, views, and forms.
* Redis caching configuration optimized for product categories and individual products, alongside automated cache invalidation handled via Django Signals.
* Hardened security settings including rate limiting protection, environment variable integration for sensitive credentials, and production configurations.
* Containerized environment setup utilizing a Dockerfile and docker-compose.yml configuration.
* Production-ready static file handling using Gunicorn and WhiteNoise.

---

## Tech Stack

* **Backend:** Python, Django Web Framework, Django ORM, Redis (Caching)
* **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript (AJAX / Fetch API)
* **Database:** SQLite (Development)
* **DevOps & Security:** Docker, docker-compose, WhiteNoise, Gunicorn

---

## Installation & Setup

Follow these steps to set up and run the project locally.

### Prerequisites
* Python 3.10 or higher
* Docker and Docker Compose (Optional, for containerized environment)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/Peru-er/BookShop.git](https://github.com/Peru-er/BookShop.git)
   cd BookShop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrations
   python manage.py migrate
   ```

5. Create a superuser account to access the admin dashboard:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```
   Access the local application at `http://127.0.0.1:8000/`.

### Running with Docker

If you prefer to run the application using Docker and Docker Compose (which automatically handles the web app and Redis cache dependency):

1. Ensure you have Docker and Docker Compose installed.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.

---

## Future Roadmap

The following modules and features are scheduled for implementation:

* [ ] Cloud Deployment: Finalizing configuration and hosting the production build live via Render or Railway.
* [ ] Social Authentication: Integration of Google OAuth sign-in methods via `django-allauth`.
* [ ] PDF Invoice Generation: Generating structured order invoices using ReportLab or WeasyPrint sent via email attachment.
* [ ] Analytics Dashboard: Building a custom administrative dashboard with visual charts (Chart.js) to track key sales metrics, performance KPIs, and top-selling items.
* [ ] CI/CD Pipeline: Configuring GitHub Actions workflow automation for testing, code linting, and automated deployment updates.