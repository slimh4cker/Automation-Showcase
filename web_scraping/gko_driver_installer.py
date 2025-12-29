import os
import platform
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from dotenv import load_dotenv

class GeckoDriverInstaller:
    def __init__(self):
        """
        Initializes the installer with the target directory where GeckoDriver
        will be installed permanently, as defined in the .env file.
        """
        load_dotenv()

        self.geckodriver_path = os.getenv('GECKODRIVER_PATH')
        if not self.geckodriver_path:
            raise ValueError("GeckoDriver path not set in the .env file.")

        self.target_dir = Path(self.geckodriver_path)

        if not self.target_dir.exists():
            raise FileNotFoundError(f"The target directory {self.target_dir} does not exist.")
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"The target path {self.target_dir} is not a directory.")

        self.download_url = None
        self.download_path = None

    def get_download_url(self) -> str:
        """
        Determines the download URL for GeckoDriver based on the operating system.
        :return: The URL to download the appropriate GeckoDriver version.
        """
        system = platform.system().lower()

        if system == "windows":
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip"
        elif system == "darwin":
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-macos.tar.gz"
        elif system == "linux":
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz"
        else:
            raise OSError("Unsupported operating system.")
        
        return self.download_url

    def download_geckodriver(self) -> None:
        """
        Downloads the GeckoDriver file directly into the target directory.
        """
        self.get_download_url()
        filename = self.download_url.split("/")[-1]
        self.download_path = self.target_dir / filename

        print(f"Downloading GeckoDriver from {self.download_url}...")
        urllib.request.urlretrieve(self.download_url, self.download_path)
        print(f"Download completed: {self.download_path}")

    def extract_file(self) -> None:
        """
        Extracts the downloaded file depending on its type (zip or tar.gz)
        directly into the target directory.
        """
        print(f"Extracting the file {self.download_path}...")

        if not self.download_path.exists():
            raise FileNotFoundError(f"The downloaded file {self.download_path} does not exist.")

        if self.download_path.suffix == ".zip":
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(self.target_dir)
        elif self.download_path.name.endswith(".tar.gz"):
            with tarfile.open(self.download_path, 'r:gz') as tar_ref:
                tar_ref.extractall(self.target_dir)
        else:
            raise ValueError("Unsupported file format. It must be .zip or .tar.gz.")

        print(f"Extraction completed in: {self.target_dir}")

    def clean_up(self) -> None:
        """
        Cleans up the downloaded archive file after extraction.
        """
        if self.download_path and self.download_path.exists():
            self.download_path.unlink()
            print(f"Removed temporary file: {self.download_path}")

    def install(self) -> None:
        """
        Executes the installation process: download, extraction, and cleanup.
        """
        try:
            self.download_geckodriver()
            self.extract_file()
            self.clean_up()
            print("GeckoDriver installed and configured successfully!")
        except Exception as e:
            print(f"An error occurred during installation: {e}")
            self.clean_up()


# Running the script
if __name__ == "__main__":
    installer = GeckoDriverInstaller()  
    installer.install()
