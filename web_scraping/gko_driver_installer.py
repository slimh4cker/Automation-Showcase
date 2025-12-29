import os
import platform
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory
from dotenv import load_dotenv

class GeckoDriverInstaller:
    def __init__(self, target_dir: Path = Path.cwd()):
        """
        Initializes the installer with a target directory where GeckoDriver will be placed.
        :param target_dir: The directory where geckodriver will be moved after installation.
        """
        self.target_dir = target_dir
        self.download_url = None
        self.download_path = None
        self.extract_path = None
        load_dotenv()

        self.geckodriver_path = os.getenv('GECKODRIVER_PATH')
        if not self.geckodriver_path:
            raise ValueError("GeckoDriver path not set in the .env file.")

    def get_download_url(self) -> str:
        """
        Determines the download URL for GeckoDriver based on the operating system.
        :return: The URL to download the appropriate GeckoDriver version.
        """
        system = platform.system().lower()

        if system == "windows":
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip"
        elif system == "darwin":  # macOS
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-macos.tar.gz"
        elif system == "linux":
            self.download_url = "https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz"
        else:
            raise OSError("Unsupported operating system.")
        
        return self.download_url

    def download_geckodriver(self) -> None:
        """
        Downloads the GeckoDriver file from the determined URL.
        """
        self.get_download_url()

        with TemporaryDirectory() as temp_dir:
            self.download_path = Path(temp_dir) / "geckodriver_downloaded"
            print(f"Downloading GeckoDriver from {self.download_url}...")

            try:
                urllib.request.urlretrieve(self.download_url, self.download_path)
                print(f"Download completed: {self.download_path}")
            except Exception as e:
                raise RuntimeError(f"Error downloading GeckoDriver: {e}")

    def extract_file(self) -> None:
        """
        Extracts the downloaded file depending on its type (zip or tar.gz).
        """
        print(f"Extracting the file {self.download_path}...")

        if self.download_path.suffix == ".zip":
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                self.extract_path = self.target_dir / "geckodriver"
                zip_ref.extractall(self.extract_path)
        elif self.download_path.suffix == ".tar.gz":
            with tarfile.open(self.download_path, 'r:gz') as tar_ref:
                self.extract_path = self.target_dir / "geckodriver"
                tar_ref.extractall(self.extract_path)
        else:
            raise ValueError("Unsupported file format. It must be .zip or .tar.gz.")

        print(f"Extraction completed in: {self.extract_path}")

    def move_geckodriver(self) -> None:
        """
        Moves the geckodriver file to the target directory.
        """
        geckodriver_filename = "geckodriver" if platform.system().lower() != "windows" else "geckodriver.exe"
        extracted_geckodriver = self.extract_path / geckodriver_filename

        if not extracted_geckodriver.exists():
            raise FileNotFoundError(f"The file {geckodriver_filename} was not found in the extraction path.")

        print(f"Moving {extracted_geckodriver} to {self.target_dir}...")
        shutil.move(extracted_geckodriver, self.target_dir / geckodriver_filename)
        print(f"GeckoDriver successfully moved to: {self.target_dir / geckodriver_filename}")

    def clean_up(self) -> None:
        """
        Cleans up temporary downloaded and extracted files.
        """
        print("Cleaning up temporary files...")
        if self.download_path and self.download_path.exists():
            self.download_path.unlink()

        if self.extract_path and self.extract_path.exists():
            shutil.rmtree(self.extract_path)

    def install(self) -> None:
        """
        Executes the entire installation process: download, extraction, and moving the geckodriver file.
        """
        try:
            self.download_geckodriver()
            self.extract_file()
            self.move_geckodriver()
            self.clean_up()
            print("GeckoDriver installed and configured successfully!")
        except Exception as e:
            print(f"An error occurred during installation: {e}")
            self.clean_up()


# Running the script
if __name__ == "__main__":
    installer = GeckoDriverInstaller(target_dir=Path.cwd())  
    installer.install()
