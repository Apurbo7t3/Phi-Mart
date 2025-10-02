# 🛒 PhiMart - Online Ecommerce API

PhiMart is a simple **E-commerce REST API** built with **Django Rest Framework (DRF)**.  
It provides features like user authentication, product management, categories, cart, orders, and reviews.  
Authentication is handled using **JWT tokens** with [Djoser](https://djoser.readthedocs.io/en/latest/).

---

## 🚀 Features

- 🔐 **User Authentication**  
  - Register, login, logout  
  - JWT authentication using Djoser  

- 🛍️ **Product & Categories**  
  - List categories & products  
  - Product details with price, stock, images  

- 🛒 **Cart**  
  - Add/remove products  
  - Update quantities  

- 📦 **Orders**  
  - Create and manage orders  
  - Update order status (admin only)  
  - Cancel orders  

- ⭐ **Reviews**  
  - Add product reviews with rating & comments  
  - Only the review author can update/delete  

---

## 🛠️ Tech Stack

- **Backend:** Django, Django Rest Framework  
- **Auth:** JWT Authentication with Djoser  
- **Database:** SQLite (default) / can be replaced with PostgreSQL/MySQL  
- **Others:** Django Debug Toolbar  

---


---

## 🔧 Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/phimart.git
   cd phimart
Create & activate virtual environment

bash
Copy code
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set up environment variables
Create a .env file in the project root:

ini
Copy code
DEBUG=True
SECRET_KEY=your_django_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
Run migrations

bash
Copy code
python manage.py migrate
Create superuser

bash
Copy code
python manage.py createsuperuser
Start development server

bash
Copy code
python manage.py runserver
🔑 API Authentication
Authentication is done via JWT tokens.

Obtain token:
POST /auth/jwt/create/

Refresh token:
POST /auth/jwt/refresh/

Verify token:
POST /auth/jwt/verify/

📌 Example Endpoints
GET /products/ → List all products

GET /categories/ → List categories

POST /orders/ → Create order (authenticated users)

PATCH /orders/{id}/update_status/ → Update order status (admin only)

POST /orders/{id}/cancel/ → Cancel order

POST /products/{id}/reviews/ → Add a review for a product

🤝 Contributing
Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

