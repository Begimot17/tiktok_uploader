# TikTok Video Uploader

This Python project automates the process of uploading videos to TikTok using Selenium WebDriver. It processes videos from specific directories, uploads them to TikTok, and tracks the upload status in a JSON file.

## Features

- Automates video uploading to TikTok
- Handles multiple video formats (.mp4, .mov, .avi)
- Tracks upload status in a JSON file
- Uses Selenium with stealth techniques to bypass bot detection

## Requirements

- Python 3.8
- [Poetry](https://python-poetry.org/) for dependency management

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies:**

    ```sh
    poetry install
    ```

3. **Configure your environment:**

    Update the `ACCOUNTS_DIRECTORY` and `TIKTOK_UPLOAD_URL` constants in `main.py` as needed.

4. **Run the script:**

    ```sh
    poetry run python main.py
    ```

## Code Overview

- **`driver_init()`**: Initializes the Selenium WebDriver with custom options and stealth settings.
- **`wait_and_click_button(driver, by, value, timeout=30)`**: Waits for a button to become clickable and clicks it.
- **`open_file(filepath)`**: Opens a file using `pyautogui` to interact with file dialogs.
- **`update_json_status(file_path, file, status)`**: Updates the upload status in a JSON file.
- **`process_videos_in_directory(directory)`**: Processes and uploads videos from the specified directory, updating their upload status.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Selenium](https://www.selenium.dev/) for browser automation
- [pyautogui](https://pyautogui.readthedocs.io/) for interacting with file dialogs
- [selenium-stealth](https://github.com/diprajpatra/selenium-stealth) for bypassing bot detection
