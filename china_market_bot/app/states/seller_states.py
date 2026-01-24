"""
🏪 Seller FSM States Module

States for seller-related workflows.
"""

from aiogram.fsm.state import State, StatesGroup


class SellerStates(StatesGroup):
    """
    Seller dashboard and management states.
    """
    
    # Dashboard
    dashboard = State()
    
    # Registration flow
    registration_start = State()
    registration_company_name = State()
    registration_description = State()
    registration_phone = State()
    registration_email = State()
    registration_address = State()
    registration_inn = State()
    registration_documents = State()
    registration_confirm = State()
    registration_pending = State()
    
    # Product management
    products_list = State()
    product_view = State()
    
    # Add product
    product_add_name = State()
    product_add_description = State()
    product_add_category = State()
    product_add_price = State()
    product_add_discount = State()
    product_add_quantity = State()
    product_add_images = State()
    product_add_video = State()
    product_add_specifications = State()
    product_add_confirm = State()
    
    # Edit product
    product_edit_select_field = State()
    product_edit_name = State()
    product_edit_description = State()
    product_edit_category = State()
    product_edit_price = State()
    product_edit_discount = State()
    product_edit_quantity = State()
    product_edit_images = State()
    product_edit_confirm = State()
    
    # Orders management
    orders_list = State()
    order_view = State()
    order_update_status = State()
    order_add_tracking = State()
    order_contact_customer = State()
    
    # Analytics
    analytics_overview = State()
    analytics_products = State()
    analytics_orders = State()
    analytics_revenue = State()
    analytics_date_range = State()
    
    # Settings
    settings_menu = State()
    settings_profile = State()
    settings_notifications = State()
    settings_payment = State()
    
    # Payouts
    payouts_list = State()
    payout_request = State()
    payout_details = State()


class SellerProductStates(StatesGroup):
    """
    Product management states (alternative grouping).
    """
    
    # List and browse
    listing = State()
    viewing = State()
    
    # Create flow
    create_start = State()
    create_name = State()
    create_short_description = State()
    create_description = State()
    create_category = State()
    create_subcategory = State()
    create_price = State()
    create_discount_price = State()
    create_quantity = State()
    create_min_order = State()
    create_images = State()
    create_video = State()
    create_weight = State()
    create_specifications = State()
    create_confirm = State()
    
    # Edit flow
    edit_select = State()
    edit_field = State()
    edit_confirm = State()
    
    # Delete
    delete_confirm = State()
    
    # Duplicate
    duplicate_confirm = State()


class SellerOrderStates(StatesGroup):
    """
    Order management states.
    """
    
    # List
    listing = State()
    filtering = State()
    
    # View
    viewing = State()
    
    # Actions
    accepting = State()
    rejecting = State()
    reject_reason = State()
    
    # Fulfillment
    preparing = State()
    ready_for_pickup = State()
    shipping = State()
    add_tracking = State()
    mark_shipped = State()
    mark_delivered = State()
    
    # Communication
    contacting_customer = State()
    sending_message = State()
    
    # Issues
    reporting_issue = State()
    issue_description = State()
