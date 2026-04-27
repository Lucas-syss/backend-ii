# Django Shopping Cart

A simple shopping cart exercise built with Django and tested with pytest.

## What it does

- **Products** — stores items with a name and price
- **Cart** — users can add products to their cart
- **Order** — holds the cart, calculates the total, and tracks whether it was paid
- **Buy** — marks the order as paid, no payment integration needed

## Project structure

```
shop/        → Django config (settings, urls)
products/    → Product model and list endpoint
orders/      → Order model, cart and buy endpoints
```

## How to run

Install dependencies:
```bash
pip install -r requirements.txt
```

Create the database:
```bash
python manage.py migrate --run-syncdb
```

Run the tests:
```bash
pytest -v
```