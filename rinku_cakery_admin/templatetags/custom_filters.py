from django import template

from rinku_cakery_admin.models import Product
# from cake_shop_admin.models import Product  # Import your Product model

register = template.Library()

@register.filter
def get_value(prices_dict, key):
    return prices_dict.get(key, 'Default Price')  # Replace 'Default Price' with your default value

@register.simple_tag
def get_prices():
    prices = {}
    products = Product.objects.all()
    for product in products:
        prices[product.pweight] = product.pprice
    return prices
