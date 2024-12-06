from django import template


register = template.Library()

@register.filter
def calculate_total_price(product_totals, product_id):
    for key, value in product_totals.items():
        if key == product_id:
            return value
    return 0 

@register.filter
def get_value(prices_dict, key):
    return prices_dict.get(key, 'Default Price')  # Replace 'Default Price' with your default value

# @register.simple_tag
# def get_prices():
#     prices = {}
#     products = Product.objects.all()
#     for product in products:
#         prices[product.pweight] = product.pprice
#     return prices



# @register.filter
# def get_total_price(product_totals, product_id):
#     print(f"Product Totals: {product_totals}")
#     print(f"Product ID: {product_id}")
#     for product_id_in_list, total_price in product_totals:
#         if product_id_in_list == product_id:
#             return total_price
#     return 0  # Default value if product ID not found