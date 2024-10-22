import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import requests
import simple_term_menu
from bs4 import BeautifulSoup
from PIL import Image, ImageFile
from tqdm import tqdm

BASE_URL = "https://readallcomics.com"
COMICS_FOLDER = "Comics"


# Utility Functions
def sanitize_name(name: str) -> str:
    """Sanitizes a name by removing special characters."""
    return name.replace("/", "-").replace("(", "").replace(")", "")


def fetch_page(url: str) -> BeautifulSoup:
    """Fetches a webpage and returns its BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_image(img_url: str) -> requests.Response:
    """Fetches an image from a URL."""
    full_url = f"https:{img_url}" if img_url.startswith("//") else img_url
    try:
        return requests.get(full_url, timeout=10)
    except requests.RequestException as e:
        print(f"Error fetching image {img_url}: {e}")
        return None


def process_image(img_response: requests.Response) -> Image.Image:
    """Resizes the image to a width of 800 pixels while maintaining aspect ratio."""
    if img_response and img_response.status_code == 200:
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        width, height = img.size
        new_height = int((800 / width) * height)
        return img.resize((800, new_height), Image.LANCZOS)
    return None


def download_single_issue(url: str, file_path: str):
    """Downloads a single comic issue and saves it as a PDF."""
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    soup = fetch_page(url)
    if not soup:
        print(f"Skipping {url} due to fetch error.")
        return

    image_urls = [img["src"] for img in soup.find_all("img")[1:-1]]
    images = [process_image(fetch_image(img_url)) for img_url in image_urls if img_url]
    images = [img for img in images if img]

    if images:
        images[0].save(
            file_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
    else:
        print(f"No images found for {url}.")


def process_comic(comic_url: str, folder: str) -> List[Tuple[str, str]]:
    """Processes a comic and returns a list of issue URLs and their file paths."""
    os.makedirs(os.path.join(COMICS_FOLDER, folder), exist_ok=True)
    with open(os.path.join(COMICS_FOLDER, folder, "url.txt"), "w") as f:
        f.write(comic_url)

    soup = fetch_page(comic_url)
    if not soup:
        return []

    list_story = soup.find("ul", {"class": "list-story"})
    if not list_story:
        print(f"No stories found in {comic_url}.")
        return []

    return [
        (
            story.a["href"],
            os.path.join(
                COMICS_FOLDER, folder, f"{sanitize_name(story.a['title'])}.pdf"
            ),
        )
        for story in list_story.find_all("li")
    ]


def get_comic_urls(folder: str) -> List[Tuple[str, str]]:
    """Retrieves comic URLs from a folder."""
    url_file = os.path.join(COMICS_FOLDER, folder, "url.txt")
    if not os.path.isfile(url_file):
        return []

    with open(url_file, "r") as f:
        url = f.read().strip()

    return process_comic(url, folder)


def update_comics():
    """Checks for updates and downloads missing issues."""
    folders = [
        folder
        for folder in os.listdir(COMICS_FOLDER)
        if os.path.isdir(os.path.join(COMICS_FOLDER, folder))
    ]
    with ThreadPoolExecutor() as executor:
        updates = list(
            tqdm(
                executor.map(get_comic_urls, folders),
                desc="Checking updates",
                total=len(folders),
            )
        )

    update_list = [
        item for sublist in updates for item in sublist if not os.path.exists(item[1])
    ]
    with ThreadPoolExecutor() as executor:
        list(
            tqdm(
                executor.map(lambda x: download_single_issue(*x), update_list),
                desc="Updating comics",
                total=len(update_list),
            )
        )


def search_comics(search_term: str):
    """Searches for comics matching the search term."""
    search_url = f"{BASE_URL}/?story={search_term}&s=&type=comic"
    soup = fetch_page(search_url)
    if not soup:
        return None
    return soup.find("ul", {"class": "list-story"})


def search_and_download(args):
    """Searches for comics and downloads selected issues."""
    comic_list = search_comics(args.search)
    if not comic_list:
        print("No comics found.")
        return

    comic_list = comic_list.find_all("li")
    if args.select:
        options = [comic.a["title"] for comic in comic_list]
        menu = simple_term_menu.TerminalMenu(
            options, multi_select=True, show_multi_select_hint=True
        )
        selected_indices = menu.show()
        comic_list = [comic_list[i] for i in selected_indices]

    download_list = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_comic, comic.a["href"], sanitize_name(comic.a["title"])
            )
            for comic in comic_list
        ]
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing comics"
        ):
            download_list.extend(future.result())

    download_list = [
        (url, path) for url, path in download_list if not os.path.exists(path)
    ]
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(download_single_issue, url, path)
            for url, path in download_list
        ]
        list(tqdm(as_completed(futures), total=len(futures), desc="Downloading"))
