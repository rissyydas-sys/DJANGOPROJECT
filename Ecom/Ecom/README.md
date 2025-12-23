# Ecom (Django) - Sample E-commerce Project

This is a sample Django project that implements an e-commerce data model with:
- Product
- Order
- OrderItem
- (Using Django built-in User model)

Features:
- SQLite3 database (default Django configuration)
- Admin change list pages for Products and Orders show items as *cards*
- Simple user-facing pages (Products and My Orders) displaying cards
- Sample fixture to create a staff user and products

## Setup

1. Make sure you have Python 3.8+ and pip installed.
2. Install Django:
   ```bash
   pip install django
   ```
3. Extract the project and `cd` into the `Ecom` folder.
4. Create migrations and migrate:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. (Optional) Load sample data:
   ```bash
   python manage.py loaddata store/fixtures/sample_data.json
   ```
   Note: sample user has a fake password hash. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Open:
   - User pages: http://127.0.0.1:8000/
   - Orders (user must be logged in): http://127.0.0.1:8000/orders/
   - Admin: http://127.0.0.1:8000/admin/

## Notes

- Admin card views are implemented by replacing the change_list template for the Product and Order ModelAdmins.
- Customize `SECRET_KEY` in `Ecom/settings.py` for production use.
- This project uses inline CSS for the card layouts for simplicity.
