import concurrent.futures
import os
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import simple_term_menu

BASE_URL = "https://readallcomics.com"
COMICS_DIR = "Comics"

def _fetch_page(url: str) -> BeautifulSoup:
    """Fetch and parse a web page."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def _search_comics(search_term: str) -> BeautifulSoup:
    """Search for comics based on a search term."""
    search_url = f"{BASE_URL}/?story={search_term}&s=&type=comic"
    return _fetch_page(search_url).find("ul", {"class": "list-story"})

def _sanitize_folder_name(folder: str) -> str:
    """Sanitize folder name for file system compatibility."""
    return folder.replace("/", "-").replace("(", "").replace(")", "")

def _get_comic_info(comic_url: str, folder: str) -> List[Tuple[str, str]]:
    """Get comic information and prepare download list."""
    comic_folder = os.path.join(COMICS_DIR, _sanitize_folder_name(folder))
    os.makedirs(comic_folder, exist_ok=True)
    
    with open(os.path.join(comic_folder, "url.txt"), "w") as f:
        f.write(comic_url)
    
    soup = _fetch_page(comic_url)
    list_story = soup.find("ul", {"class": "list-story"})
    
    if list_story:
        return [
            (story.a["href"], os.path.join(comic_folder, f"{story.a['title'].replace('/', '-')}.pdf"))
            for story in list_story.find_all("li")
        ]
    return []

def download_issue(url: str, file_path: str):
    """Download a single comic issue."""
    import subprocess
    subprocess.run(["python", "download_single_issue.py", "--url", url, "--file_path", file_path])

def search_and_download(search: str, download: bool, select: bool, with_url: bool):
    """Search for comics and optionally download them."""
    comic_list = _search_comics(search)
    if not comic_list:
        print("No comics found.")
        return

    comics = comic_list.find_all("li")

    if not download:
        _display_search_results(comics, with_url)
        return

    if select:
        comics = _select_comics(comics)

    download_list = _get_download_list(comics)
    _download_comics(download_list)

def _display_search_results(comics: List[BeautifulSoup], with_url: bool):
    """Display search results."""
    for comic in comics:
        title = comic.a["title"]
        url = comic.a["href"] if with_url else ""
        print(f"{title:<60} {url}".strip())
        print()

def _select_comics(comics: List[BeautifulSoup]) -> List[BeautifulSoup]:
    """Allow user to select comics from search results."""
    options = [comic.a["title"] for comic in comics]
    menu = simple_term_menu.TerminalMenu(options, multi_select=True, show_multi_select_hint=True)
    selected_indices = menu.show()
    return [comics[i] for i in selected_indices]

def _get_download_list(comics: List[BeautifulSoup]) -> List[Tuple[str, str]]:
    """Prepare download list for selected comics."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_get_comic_info, comic.a["href"], comic.a["title"]) for comic in comics]
        download_list = [
            item for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing comics")
            for item in future.result()
        ]
    
    return [(url, file_path) for url, file_path in download_list if not os.path.exists(file_path)]

def _download_comics(download_list: List[Tuple[str, str]]):
    """Download comics from the prepared list."""
    download_list.sort(key=lambda x: x[1])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda x: download_issue(*x), download_list), total=len(download_list), desc="Downloading"))

def update_comics():
    """Update existing comics with new issues."""
    update_required_list = _get_update_list()
    _download_comics(update_required_list)

def _get_update_list() -> List[Tuple[str, str]]:
    """Get list of comics that need updating."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        update_required_list = list(tqdm(
            executor.map(_get_comic_urls, sorted(os.listdir(COMICS_DIR))),
            desc="Checking updates",
            total=len(os.listdir(COMICS_DIR)),
            miniters=1
        ))
    
    update_required_list = [item for sublist in update_required_list for item in sublist]
    update_required_list.sort(key=lambda x: x[1])
    return update_required_list

def _get_comic_urls(folder: str) -> List[Tuple[str, str]]:
    """Get URLs for new issues of a comic."""
    url_file = os.path.join(COMICS_DIR, folder, "url.txt")
    if not os.path.isfile(url_file):
        return []

    with open(url_file, "r") as f:
        url = f.read().strip()
    
    try:
        soup = _fetch_page(url)
        list_story = soup.find("ul", {"class": "list-story"})
    except:
        return []

    if not list_story:
        return []

    return [
        (story.a["href"], os.path.join(COMICS_DIR, folder, f"{story.a['title'].replace('/', '-')}.pdf"))
        for story in list_story.find_all("li")
        if not os.path.exists(os.path.join(COMICS_DIR, folder, f"{story.a['title'].replace('/', '-')}.pdf"))
    ]

def download_comic(url, folder):
    sanitized_folder = _sanitize_folder_name(folder)
    comic_folder = os.path.join(COMICS_DIR, sanitized_folder)
    os.makedirs(comic_folder, exist_ok=True)
    with open(os.path.join(comic_folder, "url.txt"), "w") as f:
        f.write(url)
    
    soup = _fetch_page(url)
    list_story = soup.find("ul", {"class": "list-story"})

    if list_story:
        stories = list_story.find_all("li")
        download_list = [
            (story.a["href"], os.path.join(comic_folder, f"{story.a['title'].replace('/', '-')}.pdf"))
            for story in stories
        ]
        _download_comics(download_list)