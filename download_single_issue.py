"""
Downloads a single issue from a given URL and saves it as a PDF.

Args:
    url (str): The URL of the issue to download.
    file_path (str): The file path to save the downloaded issue.

Raises:
    requests.exceptions.HTTPError: If there is an error fetching the image URLs.
"""

import argparse
import io

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFile


def fetch_image(img_url):
    full_url = f"https:{img_url}" if img_url.startswith("//") else img_url
    return requests.get(full_url)


def process_image(img_response):
    if img_response.status_code != 200:
        return None
    img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
    width, height = img.size
    new_height = int((800 / width) * height)
    return img.resize((800, new_height), Image.LANCZOS)


def download_single_issue(url, file_path):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    image_urls = [img["src"] for img in soup.find_all("img")[1:-1]]
    images = []
    for img_url in image_urls:
        img_response = fetch_image(img_url)
        img = process_image(img_response)
        if img:
            images.append(img)
    if len(images) != 0:
        images[0].save(
            file_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download a single issue from a given URL and save it as a PDF."
    )
    parser.add_argument("--url", help="The URL of the issue to download")
    parser.add_argument(
        "--file_path", help="The file path to save the downloaded issue"
    )
    args = parser.parse_args()

    download_single_issue(args.url, args.file_path)
