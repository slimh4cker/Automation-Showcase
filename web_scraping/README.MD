# GeckoDriver Installer

This Python script automates the process of downloading, extracting, and setting up **GeckoDriver** for use with **Selenium**. It works by detecting your operating system and downloading the correct version of **GeckoDriver** (Windows, macOS, or Linux), extracting it, and placing it in a directory of your choice. The **GeckoDriver** path is configured via a `.env` file to keep it flexible and easily configurable.

### Install Dependencies

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```
### Dependencies:

- selenium
- beautifulsoup4
- pandas
- python-dotenv: For managing environment variables from the .env file.

### Setup

Create a .env file in the root directory of your project and define the GECKODRIVER_PATH variable:

```bash
GECKODRIVER_PATH=/path/to/geckodriver
```

Run the script:

```bash
python install_geckodriver.py
```
