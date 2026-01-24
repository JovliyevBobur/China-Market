"""
📋 Order FSM States Module

States for order-related workflows.
"""

from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """
    Order creation and management states.
    """
    
    # Cart review
    cart_review = State()
    cart_update = State()
    
    # Contact info
    entering_name = State()
    entering_phone = State()
    confirming_phone = State()
    entering_email = State()
    
    # Delivery
    selecting_delivery_type = State()
    entering_address = State()
    entering_city = State()
    entering_region = State()
    entering_postal_code = State()
    selecting_pickup_point = State()
    
    # Delivery date/time
    selecting_delivery_date = State()
    selecting_delivery_time = State()
    
    # Notes
    entering_notes = State()
    
    # Promo code
    entering_promo_code = State()
    
    # Payment
    selecting_payment_method = State()
    processing_payment = State()
    waiting_payment = State()
    payment_callback = State()
    
    # Confirmation
    order_summary = State()
    confirming_order = State()
    
    # Completed
    order_placed = State()
    order_confirmed = State()
    
    # Tracking
    tracking_order = State()
    
    # Post-order
    rating_order = State()
    leaving_review = State()


class CheckoutStates(StatesGroup):
    """
    Checkout process states (alternative grouping).
    """
    
    # Start
    start = State()
    
    # Cart validation
    validating_cart = State()
    updating_prices = State()
    removing_unavailable = State()
    
    # Customer info
    customer_info = State()
    name = State()
    phone = State()
    email = State()
    
    # Shipping
    shipping_method = State()
    shipping_address = State()
    address_line1 = State()
    address_line2 = State()
    city = State()
    region = State()
    postal_code = State()
    
    # Pickup
    pickup_point = State()
    
    # Summary
    summary = State()
    
    # Promo
    promo_code = State()
    applying_promo = State()
    
    # Payment
    payment_method = State()
    payment_processing = State()
    payment_3ds = State()
    payment_waiting = State()
    
    # Telegram Stars
    stars_invoice = State()
    stars_waiting = State()
    
    # Click/Payme
    external_payment = State()
    external_waiting = State()
    
    # Cash
    cash_confirmation = State()
    
    # Final
    placing_order = State()
    success = State()
    failed = State()


class PaymentStates(StatesGroup):
    """
    Payment processing states.
    """
    
    # Method selection
    selecting_method = State()
    
    # Telegram Stars
    stars_amount = State()
    stars_invoice = State()
    stars_processing = State()
    
    # Card payment
    card_input = State()
    card_processing = State()
    card_3ds = State()
    
    # External providers
    payme_redirect = State()
    payme_waiting = State()
    click_redirect = State()
    click_waiting = State()
    
    # Cash
    cash_amount = State()
    cash_confirmation = State()
    
    # Result
    success = State()
    failed = State()
    cancelled = State()
    
    # Refund
    refund_request = State()
    refund_amount = State()
    refund_reason = State()
    refund_processing = State()


class OrderHistoryStates(StatesGroup):
    """
    Order history viewing states.
    """
    
    # List
    listing = State()
    filtering = State()
    
    # View
    viewing = State()
    viewing_items = State()
    viewing_tracking = State()
    
    # Actions
    reordering = State()
    cancelling = State()
    cancel_reason = State()
    
    # Review
    rating = State()
    reviewing = State()
    
    # Support
    contacting_support = State()
    support_message = State()
