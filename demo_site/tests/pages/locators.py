# from selenium.webdriver.common.by import By


# for maintainability, we can separate web objects by page name

class InventoryLocators():
    list_of_products = ('class name', 'inventory_item_name ')
    cart = ('id', 'shopping_cart_container')
    add_to_cart = ('id', 'add-to-cart-{product_name}')
    burger_menu = ('id', 'react-burger-menu-btn')
    shopping_cart = ('class name', 'shopping_cart_link')


# class LoginPageLocators():
#     username = ('id', 'user-name')
#     password = ('id', 'password')
#     submit = ('id', 'login-button')
#     error_message = ('id', 'message_error')


class CartLocators():
    cart_container = ('class name', 'cart_list')
    items_in_cart = ('class name', 'inventory_item_name')


class LoginPageLocators():
    user_id = ('id', 'input')
    next = ('id', 'verifUseridBtn')
    password = ('type', 'password')
    sign_in = ('id', 'signBtn')
    common_alert = ('id', 'common_alert')


class NavigatorLocators():
    home = ('href', '#/home')
