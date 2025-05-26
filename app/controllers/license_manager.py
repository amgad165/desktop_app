from app.models.app_models import session, License
from app.controllers.hardware_id import get_hardware_id

def is_license_active():
    """Check if the stored license matches the current device."""
    hardware_id = get_hardware_id()
    license_entry = session.query(License).filter_by(is_active=True, hardware_id=hardware_id).first()
    return license_entry is not None

def activate_license(license_key):
    """Activate the license only if the hardware ID matches"""
    predefined_keys = ["aaa", "ddd","mo","wahba","mohamed", "12345678910", "M0H4M3D2024"]  # Replace with real keys
    hardware_id = get_hardware_id()

    if license_key in predefined_keys:
        existing_license = session.query(License).first()
        
        if existing_license:
            if existing_license.hardware_id == hardware_id:
                existing_license.is_active = True
                session.commit()
                return True  # Activation successful
            else:
                return False  # License key already used on another device
        else:
            new_license = License(license_key=license_key, hardware_id=hardware_id, is_active=True)
            session.add(new_license)
            session.commit()
            return True  # Activation successful

    return False  # Invalid license key
