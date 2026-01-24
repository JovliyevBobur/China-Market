"""
👤 User FSM States Module

States for user-related workflows.
"""

from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    """
    General user states.
    """
    
    # Main menu
    main_menu = State()
    
    # Catalog browsing
    browsing_catalog = State()
    viewing_category = State()
    viewing_product = State()
    
    # Search
    searching = State()
    search_results = State()
    
    # Cart
    viewing_cart = State()
    editing_cart_item = State()
    
    # Favorites
    viewing_favorites = State()


class RegistrationStates(StatesGroup):
    """
    User registration states.
    """
    
    # Language selection
    selecting_language = State()
    
    # Phone number
    entering_phone = State()
    confirming_phone = State()
    
    # Name
    entering_name = State()
    
    # Terms
    accepting_terms = State()
    
    # Completed
    completed = State()


class ProfileStates(StatesGroup):
    """
    Profile editing states.
    """
    
    # View profile
    viewing_profile = State()
    
    # Edit fields
    editing_name = State()
    editing_phone = State()
    editing_email = State()
    editing_language = State()
    
    # Address
    editing_address = State()
    
    # Settings
    editing_settings = State()
    editing_notifications = State()


class SearchStates(StatesGroup):
    """
    Search states.
    """
    
    # Input query
    entering_query = State()
    
    # Filters
    selecting_category = State()
    setting_price_range = State()
    setting_min_price = State()
    setting_max_price = State()
    
    # Results
    viewing_results = State()
    
    # Sort
    selecting_sort = State()


class ReviewStates(StatesGroup):
    """
    Review creation states.
    """
    
    # Rating
    selecting_rating = State()
    
    # Content
    entering_title = State()
    entering_content = State()
    
    # Pros/Cons
    entering_pros = State()
    entering_cons = State()
    
    # Images
    uploading_images = State()
    
    # Confirm
    confirming_review = State()


class SupportStates(StatesGroup):
    """
    Support/Help states.
    """
    
    # Topic selection
    selecting_topic = State()
    
    # Message
    entering_message = State()
    
    # Order related
    selecting_order = State()
    
    # Confirmation
    confirming_request = State()
    
    # Waiting response
    waiting_response = State()
