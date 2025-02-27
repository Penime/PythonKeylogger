# PythonKeylogger

This project is a keylogger application that records keystrokes from multiple computers and users, stores the data on a server, and provides a web-based interface to view and analyze the recorded data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Front-End Interface](#front-end-interface)
- [License](#license)
- [Contributing](#contributing)

## Features

- Records keystrokes from multiple computers and users.
- Stores recorded data in a JSON file on the server.
- Provides a web-based interface to view and analyze the recorded data.
- Supports filtering and searching of recorded data.
- Displays insights such as extracted emails and URLs from the recorded data.
- Supports dark and light themes for the web interface.

## System Requirements

- Python 3.x
- `pip` installed

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/Penime/PythonKeylogger.git
   ```

2. Navigate to the project directory:

   ```shell
   cd PythonKeylogger
   ```

3. Create a virtual environment (*optional*):

   ```shell
   python -m venv .venv
   ```

4. Activate the virtual environment (*optional*):

   - On Windows:
     ```shell
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```shell
     source .venv/bin/activate
     ```

5. Install dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Start the server inside the `server` directory:

   ```shell
   python run_server.py
   ```

2. Run the Keylogger by executing the main script in the `key_logger` directory:

   ```shell
   python main.py
   ```

3. open `frontend/index.html` in your browser.

## API Endpoints

- `GET /data`: Returns all keylog data as JSON.
- `GET /computers`: Returns a list of computers and users (no logs).
- `GET /user_data`: Returns logs for a specific user.
- `POST /logs`: Receives and stores keylog data from clients.

## Front-End Interface

The front-end interface provides the following features:

- **Data Viewer**: Displays a list of computers and users with recorded data.
- **User Details**: Displays detailed logs and insights for a selected user.
- **Filtering and Searching**: Allows filtering and searching of recorded data.
- **Insights**: Extracts and displays emails and URLs from the recorded data.
- **Theme Toggle**: Supports dark and light themes.

## Logging & Storage

- If configured captured keystrokes can be stored in a local log file.
- logs is sent to a remote server.
- Ensure that logs are managed securely and deleted if necessary.

## Uninstallation

1. Delete the project directory:

   ```shell
   rm -rf PythonKeylogger
   ```

2. If a virtual environment was created, remove it:

   ```shell
   rm -rf .venv
   ```

3. Remove any generated log files:

   ```shell
   rm logs.txt
   ```

## Security & Ethical Disclaimer

The use of a Keylogger may violate privacy rights and laws. This tool is intended for ethical use only, such as monitoring personal devices with explicit consent. Ensure compliance with local laws before using this software.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributing

Contributions are welcome! To contribute:

- Fork the repository.
- Create a new branch.
- Commit and push your changes.
- Submit a pull request.

For any issues or feature requests, open an issue in the repository.
