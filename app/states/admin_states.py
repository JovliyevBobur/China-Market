"""
👑 Admin FSM States Module

States for admin-related workflows.
"""

from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    """
    Admin panel states.
    """
    
    # Dashboard
    dashboard = State()
    
    # User management
    users_list = State()
    user_search = State()
    user_view = State()
    user_ban = State()
    user_ban_reason = State()
    user_unban = State()
    user_change_role = State()
    user_send_message = State()
    
    # Seller management
    sellers_list = State()
    seller_pending = State()
    seller_view = State()
    seller_approve = State()
    seller_reject = State()
    seller_reject_reason = State()
    seller_suspend = State()
    seller_suspend_reason = State()
    
    # Product moderation
    moderation_pending = State()
    moderation_view = State()
    moderation_approve = State()
    moderation_reject = State()
    moderation_reject_reason = State()
    
    # Category management
    categories_list = State()
    category_view = State()
    category_add_name = State()
    category_add_name_uz = State()
    category_add_name_ru = State()
    category_add_name_en = State()
    category_add_parent = State()
    category_add_icon = State()
    category_add_image = State()
    category_add_confirm = State()
    category_edit = State()
    category_delete = State()
    category_delete_confirm = State()
    
    # Order management
    orders_list = State()
    order_view = State()
    order_update_status = State()
    order_add_note = State()
    order_refund = State()
    order_refund_amount = State()
    order_refund_reason = State()
    
    # Broadcast
    broadcast_select_audience = State()
    broadcast_message = State()
    broadcast_add_button = State()
    broadcast_button_text = State()
    broadcast_button_url = State()
    broadcast_preview = State()
    broadcast_confirm = State()
    broadcast_progress = State()
    
    # Statistics
    stats_overview = State()
    stats_users = State()
    stats_orders = State()
    stats_revenue = State()
    stats_products = State()
    stats_date_range = State()
    
    # Settings
    settings_menu = State()
    settings_general = State()
    settings_payment = State()
    settings_notifications = State()
    settings_security = State()
    
    # Promo codes
    promo_list = State()
    promo_add = State()
    promo_add_code = State()
    promo_add_discount = State()
    promo_add_type = State()
    promo_add_limit = State()
    promo_add_dates = State()
    promo_add_confirm = State()
    promo_edit = State()
    promo_delete = State()
    
    # Reports
    report_generate = State()
    report_type = State()
    report_date_range = State()
    report_format = State()
    report_download = State()
    
    # Support
    support_tickets = State()
    support_ticket_view = State()
    support_ticket_reply = State()
    support_ticket_close = State()


class BroadcastStates(StatesGroup):
    """
    Broadcast message states (detailed).
    """
    
    # Audience selection
    select_audience = State()
    select_language = State()
    select_role = State()
    select_activity = State()
    
    # Message content
    message_text = State()
    message_photo = State()
    message_video = State()
    message_document = State()
    
    # Buttons
    add_buttons = State()
    button_text = State()
    button_url = State()
    button_callback = State()
    
    # Preview and send
    preview = State()
    schedule = State()
    schedule_datetime = State()
    confirm = State()
    sending = State()
    completed = State()


class ModerationStates(StatesGroup):
    """
    Moderation workflow states.
    """
    
    # Queue
    queue = State()
    
    # Product review
    reviewing_product = State()
    checking_images = State()
    checking_description = State()
    checking_price = State()
    
    # Decision
    approve = State()
    reject = State()
    reject_reason_select = State()
    reject_reason_custom = State()
    
    # Request changes
    request_changes = State()
    changes_description = State()
    
    # Seller review
    reviewing_seller = State()
    checking_documents = State()
    
    # Completed
    decision_made = State()
