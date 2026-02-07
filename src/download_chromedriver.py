#!/usr/bin/env python3

import os
import shutil
import sys
import platform
import subprocess
import zipfile
import tarfile
import requests
from pathlib import Path
from typing import Optional, Tuple
import logging

from src.utils.get_os import get_os
from src.utils.get_arch import get_arch
from src.constants import OperatingSystem, OS_ARCH_MAP

logging.basicConfig(level=logging.INFO)

CHROMEDRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com"
CHROMEDRIVER_LATEST_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

def _parse_major_version(version_output: str) -> str:
    version = version_output.strip().split()[-1]
    return version.split(".")[0]

def _get_chrome_version_macos() -> Optional[str]:
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return _parse_major_version(result.stdout)
    return None

def _get_chrome_version_linux() -> Optional[str]:
    for binary in ("google-chrome", "chromium", "chromium-browser"):
        try:
            result = subprocess.run(
                [binary, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return _parse_major_version(result.stdout)
        except FileNotFoundError:
            continue
    return None

def _get_chrome_version_windows() -> Optional[str]:
    import winreg

    registry_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Google\Chrome\BLBeacon"),
    ]

    for root, path in registry_paths:
        try:
            with winreg.OpenKey(root, path) as key:
                version, _ = winreg.QueryValueEx(key, "version")
                return version.split(".")[0]
        except FileNotFoundError:
            continue
    return None

def _get_chrome_version() -> Optional[str]:
    try:
        os_ = get_os()

        if os_ == OperatingSystem.MACOS:
            return _get_chrome_version_macos()
        if os_ == OperatingSystem.LINUX:
            return _get_chrome_version_linux()
        if os_ == OperatingSystem.WINDOWS:
            return _get_chrome_version_windows()

    except Exception:
        logging.exception("Error detecting Chrome version")

    return None

def _get_latest_chromedriver_version():
    try:
        response = requests.get(CHROMEDRIVER_LATEST_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        stable_version = data.get("channels", {}).get("Stable", {}).get("version")
        return stable_version
    except Exception as e:
        logging.exception(f"Error getting latest ChromeDriver version: {e}")
        return None



def _get_chromedriver_download_url(version: str) -> Tuple[str, str]:
    os_ = get_os()
    arch = get_arch()

    os_arch = OS_ARCH_MAP[os_][arch]
    ext = "zip"

    url = (
        "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/"
        f"{version}/{os_arch}/chromedriver-{os_arch}.{ext}"
    )

    return url, ext

def download_file(url, filepath):
    logging.info(f"Downloading ChromeDriver from: {url}")
    
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    logging.info("Progress: %.1f%%", percent)
    
    logging.info("Download completed")
    return filepath


def extract_chromedriver(archive_path, extract_to, ext):
    logging.info(f"Extracting ChromeDriver from {archive_path}...")
    
    if ext == "zip":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif ext == "tar.gz":
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    
    os.remove(archive_path)
    
    for root, _, files in os.walk(extract_to):
        for file in files:
            if file == "chromedriver" or file == "chromedriver.exe":
                chromedriver_path = os.path.join(root, file)
                final_path = os.path.join(extract_to, file)
                if chromedriver_path != final_path:
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(chromedriver_path, final_path)

                # Remove apenas a pasta extraída do zip (ex: chromedriver-mac-arm64),
                # não o resto do conteúdo de extract_to
                if os.path.exists(root) and os.path.realpath(root) != os.path.realpath(extract_to):
                    shutil.rmtree(root)

                return final_path

    return None


def make_executable(filepath):
    if platform.system() != "windows":
        os.chmod(filepath, 0o755)


def main():
    logging.info("=" * 60)
    logging.info("Download ChromeDriver")
    logging.info("=" * 60)
    
    project_root = Path(__file__).parent
    chromedriver_path = project_root / "chromedriver"
    
    if chromedriver_path.exists():
        response = input(f"ChromeDriver already exists in {chromedriver_path}. Do you want to replace it? (y/N): ")
        if response.lower() != 's':
            logging.info("Operation cancelled.")
            return
        os.remove(chromedriver_path)
    
    chrome_version = _get_chrome_version()
    if chrome_version:
        logging.info(f"Chrome version detected: {chrome_version}")
    
    logging.info("Getting latest ChromeDriver version...")
    latest_version = _get_latest_chromedriver_version()
    
    if not latest_version:
        logging.error("Error getting latest ChromeDriver version")
        sys.exit(1)
    
    logging.info(f"Latest ChromeDriver version: {latest_version}")
    
    try:
        download_url, ext = _get_chromedriver_download_url(latest_version)
    except Exception as e:
        logging.error(f"Error getting download URL: {e}")
        sys.exit(1)
    
    temp_file = project_root / f"chromedriver_temp.{ext}"
    
    try:
        download_file(download_url, temp_file)
        
        chromedriver_extracted = extract_chromedriver(temp_file, project_root, ext)
        
        if chromedriver_extracted:
            if chromedriver_extracted != str(chromedriver_path):
                if chromedriver_path.exists():
                    os.remove(chromedriver_path)
                os.rename(chromedriver_extracted, chromedriver_path)
            
            make_executable(chromedriver_path)
            
            logging.info(f"\n✓ ChromeDriver downloaded successfully!")
            logging.info(f"  Location: {chromedriver_path}")
            logging.info(f"  Version: {latest_version}")
        else:
            logging.error("Error extracting ChromeDriver.")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading ChromeDriver: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if temp_file.exists():
            os.remove(temp_file)


if __name__ == "__main__":
    main()
