import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт в страйпе."""

    return stripe.Product.create(
        name=product.title,
        description=product.description,
        images=[product.preview.url] if product.preview else None,
    )


def create_stripe_price(product_id, amount):
    """Создает цену в страйпе."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"},
        product=product_id,
    )


def create_stripe_session(price_id):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )
    return session
