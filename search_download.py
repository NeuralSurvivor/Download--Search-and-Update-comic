"""
Searches for and downloads comics from readallcomics.com.

Usage:
    python search_download.py --search <term> [--download] [--with-url]
"""

import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://readallcomics.com"
COMICS_DIR = "Comics"


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def search_comics(search_term):
    search_url = f"{BASE_URL}/?story={search_term}&s=&type=comic"
    soup = fetch_page(search_url)
    return soup.find("ul", {"class": "list-story"})


def process_comic(comic_url, folder):
    try:
        soup = fetch_page(comic_url)
        list_story = soup.find("ul", {"class": "list-story"})
        if list_story:
            return [
                (
                    story.a["href"],
                    os.path.join(
                        COMICS_DIR, folder, f"{story.a['title'].replace('/', '-')}.pdf"
                    ),
                )
                for story in list_story.find_all("li")
            ]
    except requests.RequestException:
        pass
    return []


def download_issue(url, file_path):
    os.system(
        f'python download_single_issue.py --url "{url}" --file_path "{file_path}"'
    )


def search_and_download(args):
    comic_list = search_comics(args.search)
    if not comic_list:
        print("No comics found.")
        return

    if args.download:
        download_list = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    process_comic,
                    comic.a["href"],
                    comic.a["title"]
                    .replace("/", "-")
                    .replace("(", "")
                    .replace(")", ""),
                )
                for comic in comic_list.find_all("li")
            ]

            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Processing comics"
            ):
                download_list.extend(future.result())
        existing_files = [
            os.path.basename(file_path)
            for url, file_path in download_list
            if os.path.exists(file_path)
        ]
        download_list = [
            (url, file_path)
            for url, file_path in download_list
            if not os.path.exists(file_path)
        ]
        if existing_files:
            print(f"{len(existing_files)} existing files:")
        download_list = sorted(download_list, key=lambda x: x[1])
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(download_issue, url, file_path)
                for url, file_path in download_list
            ]
            list(tqdm(as_completed(futures), total=len(futures), desc="Downloading"))
    else:
        for comic in comic_list.find_all("li"):
            title = comic.a["title"]
            url = comic.a["href"] if args.with_url else ""
            print(f"{title:<60} {url}".strip())
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and download comics.")
    parser.add_argument("--search", required=True, help="Search term for comics")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the comics from search results",
    )
    parser.add_argument("--with-url", action="store_true", help="Print result with URL")
    args = parser.parse_args()

    search_and_download(args)
