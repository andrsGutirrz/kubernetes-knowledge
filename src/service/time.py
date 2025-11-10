from datetime import datetime
import pytz

# Costa Rica timezone (UTC-6)
COSTA_RICA_TZ = pytz.timezone('America/Costa_Rica')


def get_current_time():
    """Returns current Costa Rica time in ISO format"""
    now = datetime.now(COSTA_RICA_TZ)
    return now.isoformat()


def get_greeting(hour: int) -> str:
    """Returns a greeting based on the hour of the day"""
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"


def get_greeting_message(name: str = None) -> str:
    """Returns a greeting message based on current time in Costa Rica"""
    # Get current Costa Rica time
    cr_now = datetime.now(COSTA_RICA_TZ)
    
    # Get hour in Costa Rica timezone
    hour = cr_now.hour
    
    # Get greeting based on hour
    greeting = get_greeting(hour)
    
    # Use name if provided, otherwise use a default
    name_to_use = name if name else "there"
    
    return f"{greeting} {name_to_use}"

