"""
Downloads a comic from a given URL and saves the individual issues to a specified folder.

Args:
    url (str): The URL of the comic to download.
    folder (str): The folder to save the downloaded comic.
"""

import argparse
import concurrent.futures
import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def download_issue(story, folder):
    title = story.a["title"].replace("/", "-")
    issue_url = story.a["href"]
    file_path = os.path.join(folder, f"{title}.pdf")

    if not os.path.exists(file_path):
        os.system(
            f'python download_single_issue.py --url "{issue_url}" --file_path "{file_path}"'
        )


def download_comic(url, folder):
    sanitized_folder = sanitize_folder_name(folder)
    comic_folder = os.path.join("Comics", sanitized_folder)
    os.makedirs(comic_folder, exist_ok=True)
    with open(os.path.join(comic_folder, "url.txt"), "w") as f:
        f.write(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    list_story = soup.find("ul", {"class": "list-story"})

    if list_story:
        stories = list_story.find_all("li")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(download_issue, story, comic_folder)
                for story in stories
            ]
            for future in tqdm(
                concurrent.futures.as_completed(futures),
                total=len(stories),
                desc=os.path.basename(comic_folder),
            ):
                future.result()


def sanitize_folder_name(folder):
    return folder.replace("/", "-").replace("(", "").replace(")", "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a comic from a given URL.")
    parser.add_argument("--url", help="The URL of the comic to download")
    parser.add_argument("--folder", help="The folder to save the downloaded comic")
    args = parser.parse_args()
    download_comic(args.url, args.folder)
