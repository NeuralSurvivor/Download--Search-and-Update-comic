"""
Updates the comics library by downloading the latest comics from provided URLs.
"""

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

COMICS_FOLDER = "Comics"


def get_comic_urls(folder: str) -> List[Tuple[str, str]]:
    url_file = os.path.join(COMICS_FOLDER, folder, "url.txt")
    if not os.path.isfile(url_file):
        return []

    with open(url_file, "r") as f:
        url = f.read().strip()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        list_story = soup.find("ul", {"class": "list-story"})
    except:
        return []

    if not list_story:
        return []

    return [
        (
            story.a["href"],
            os.path.join(
                COMICS_FOLDER, folder, f"{story.a['title'].replace('/', '-')}.pdf"
            ),
        )
        for story in list_story.find_all("li")
        if not os.path.exists(
            os.path.join(
                COMICS_FOLDER, folder, f"{story.a['title'].replace('/', '-')}.pdf"
            )
        )
    ]


def download_single_issue(url: str, file_path: str):
    subprocess.run(
        ["python", "download_single_issue.py", "--url", url, "--file_path", file_path]
    )


def update_comics():
    update_required_list = []
    with ThreadPoolExecutor() as executor:
        update_required_list = list(
            tqdm(
                executor.map(get_comic_urls, sorted(os.listdir(COMICS_FOLDER))),
                desc="Checking updates",
                total=len(os.listdir(COMICS_FOLDER)),
                miniters=1,
            )
        )
    update_required_list = [
        item for sublist in update_required_list for item in sublist
    ]
    update_required_list = sorted(update_required_list, key=lambda x: x[1])
    with ThreadPoolExecutor() as executor:
        list(
            tqdm(
                executor.map(lambda x: download_single_issue(*x), update_required_list),
                total=len(update_required_list),
                desc="Updating comics",
                miniters=1,
            )
        )


if __name__ == "__main__":
    update_comics()
