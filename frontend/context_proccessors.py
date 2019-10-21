from .tools import initial_data


def nav_categories_data(request):
    menu_categories, cart, cart_items = initial_data(request)
    return {
        'menu_categories': menu_categories
    }