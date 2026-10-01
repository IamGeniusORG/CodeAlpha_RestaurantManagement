# CodeAlpha Restaurant Management System 🍽️

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

A full-featured, modern restaurant management backend designed to handle reservations, order processing, and dynamic inventory tracking. This project was developed as part of the **CodeAlpha Backend Development Internship**.

## ✨ Key Features

- **Elegant Public UI:** A beautifully designed, mobile-responsive customer-facing portal featuring a Digital Menu, Table Reservations, and Online Ordering.
- **Smart Reservation System:** Built-in validation logic to automatically prevent double-bookings based on active table occupancy and time slots.
- **Dynamic Inventory Engine:** Ingredients are mapped to menu items via `RecipeRequirements`. When an order is placed, the exact amount of raw ingredients is atomically deducted from the database.
- **Staff Dashboard:** A protected, real-time control center for staff to monitor active orders, visualize the floor plan's table occupancy, and track low-stock inventory alerts.
- **Transaction Safe:** Core business logic utilizes Django's `@transaction.atomic` to ensure robust data integrity during concurrent order placements.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/IamGeniusORG/CodeAlpha_RestaurantManagement.git
   cd CodeAlpha_RestaurantManagement
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your configurations:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create an Admin User**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

You can now access the application at `http://127.0.0.1:8000/`.

## 📁 Project Structure

```text
CodeAlpha_RestaurantManagement/
├── core_project/           # Main project settings and configurations
├── restaurant/             # Primary Django application
│   ├── models.py           # Database schema (Tables, Inventory, Orders)
│   ├── services.py         # Extracted business logic (Reservations, Inventory deduction)
│   ├── views.py            # Public & Staff view controllers
│   └── urls.py             # Route definitions
├── templates/              # HTML templates powered by Tailwind CSS
│   ├── public/             # Customer-facing views
│   └── staff/              # Protected staff dashboard views
└── static/                 # CSS, Images, and static assets
```

## 🔒 Security
- Sensitive configuration is isolated using `python-dotenv`.
- Staff routes are heavily protected via `UserPassesTestMixin`.
- Standard Django CSRF and XSS protections are enabled.

---
*Developed by **Tanmay Dey** for CodeAlpha.*
