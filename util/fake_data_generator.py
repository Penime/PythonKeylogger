import json
import random
import string
from datetime import datetime, timedelta

# Function to generate random key logs
def generate_key_logs():
    keys = list(string.ascii_lowercase + string.digits + "".join(" space enter backspace".split()))
    return [random.choice(keys) for _ in range(random.randint(10, 50))]

# Function to generate fake data
def generate_fake_data(computer_count=10, users_per_computer=5, apps_per_user=3, log_entries=20):
    fake_data = {}

    for i in range(computer_count):
        computer_name = f"COMPUTER-{i+1}"
        fake_data[computer_name] = {}

        for j in range(users_per_computer):
            user_name = f"User{j+1}"
            fake_data[computer_name][user_name] = {}

            for k in range(apps_per_user):
                app_name = f"App-{k+1}"
                fake_data[computer_name][user_name][app_name] = {}

                # Generate random timestamps
                base_time = datetime.now()
                for l in range(log_entries):
                    timestamp = (base_time - timedelta(minutes=l*random.randint(1, 10))).strftime("%Y-%m-%d %H:%M:%S")
                    fake_data[computer_name][user_name][app_name][timestamp] = generate_key_logs()

    return fake_data

# Generate and save to file
fake_data = generate_fake_data(computer_count=50, users_per_computer=10, apps_per_user=5, log_entries=50)

with open("fake_data.json", "w") as file:
    json.dump(fake_data, file, indent=4)

print("Fake data generated and saved as fake_data.json")
