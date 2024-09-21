
# Comic Downloader

This project provides a set of Python scripts for searching, downloading, and managing comics from readallcomics.com.

## Scripts

### download_comic.py

Downloads a complete comic series from a given URL.

Usage:

python download_comic.py --url <comic_url> --folder <folder_name>


### search_download.py

Searches for comics and optionally downloads them.

Usage:

python search_download.py --search <term> [--download] [--with-url]


### download_single_issue.py

Downloads a single comic issue from a given URL.

Usage:

python download_single_issue.py --url <issue_url> --file_path <output_file_path>


### update_comic.py

Updates the comics library by downloading the latest issues for all comics in the Comics folder.

Usage:

python update_comic.py


## Requirements

- Python 3.6+
- Required libraries: requests, beautifulsoup4, Pillow, tqdm

Install the required libraries using:

pip install requests beautifulsoup4 Pillow tqdm


## How to Use

1. To search for comics:
   
   python search_download.py --search "Batman"
   

2. To search and download comics:
   
   python search_download.py --search "Batman" --download
   

3. To download a specific comic series:
   
   python download_comic.py --url "https://readallcomics.com/category/batman-2016/" --folder "Batman 2016"
   

4. To update your comic library with the latest issues:
   
   python update_comic.py
   

## Note

This project is for educational purposes only. Please respect copyright laws and support comic creators by purchasing their work when possible.
