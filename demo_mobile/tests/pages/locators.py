
class Locators():

    """Login Page Objects"""
    skip_sign_in_button_id = "in.amazon.mShop.android.shopping:id/skip_sign_in_button"
    username_input_ACCESSIBILITYID = 'test-Username'
    password_input_ACCESSIBILITYID = 'test-Password'
    login_btn_ACCESSIBILITYID = 'test-LOGIN'

    """Products Page Objects"""
    menu_XAPTH = '//android.view.ViewGroup[@content-desc="test-Menu"]/android.view.ViewGroup/android.widget.ImageView'
    add_to_cart_XPATH = '(//android.view.ViewGroup[@content-desc="test-ADD TO CART"])[1]'
    cart_XPATH = '//android.view.ViewGroup[@content-desc="test-Cart"]/android.view.ViewGroup/android.widget.ImageView'
    toggle_products_view_XPATH = '//android.view.ViewGroup[@content-desc="test-Toggle"]/android.widget.ImageView'
    sort_icon_XPATH = '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView'
    prices_XPATH = '//android.widget.TextView[@content-desc="test-Price"]'

    """Checkout screen"""
    checkout_ACCESSIBILITYID = 'test-CHECKOUT'
    fname_ACCESSIBILITYID = 'test-First Name'
    lname_ACCESSIBILITYID = 'test-Last Name'
    zcode_ACCESSIBILITYID = 'test-Zip/Postal Code'
    cancel_ACCESSIBILITYID = 'test-CANCEL'
    continue_ACCESSIBILITYID = 'test-CONTINUE'

    def product_locator_id(self, name):
        ids = {
            'Sauce Labs Backpack': 1
        }
        return f'(//android.view.ViewGroup[@content-desc="test-ADD TO CART"])[{ids[name]}]'

def read_locator(locator_identifier):
        return eval(f"Locators.{locator_identifier}")
