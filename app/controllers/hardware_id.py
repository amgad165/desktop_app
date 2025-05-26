import uuid
import hashlib

def get_hardware_id():
    """Generate a unique hardware ID based on the MAC address."""
    mac = uuid.getnode()  # Get MAC address
    mac_str = str(mac).encode('utf-8')  # Convert to bytes
    hashed_mac = hashlib.sha256(mac_str).hexdigest()  # Hash for security
    return hashed_mac
