
# Comic Downloader

This project provides a set of Python scripts for searching, downloading, and managing comics from readallcomics.com.

## Scripts

### download_comic.py
Downloads a complete comic series from a given URL and saves individual issues as PDF files.

Usage:

```bash
python download_comic.py --url <comic_url> --folder <folder_name>
```

- `<comic_url>`: The URL of the comic series to download.
- `<folder_name>`: The name of the folder where the comic will be saved.

Features:
- Creates a folder for the comic series inside a "Comics" directory.
- Downloads all available issues of the comic series.
- Uses multithreading for faster downloads.
- Skips already downloaded issues.
- Sanitizes folder names to avoid issues with special characters.
- Saves the source URL in a text file within the comic's folder.


### search_download.py

Searches for comics and optionally downloads them.

Usage:


python search_download.py --search <term> [--download] [--with-url] [--select]


- `<term>`: The search term to find comics.
- `--download`: Optional flag to download the found comics.
- `--with-url`: Optional flag to display URLs with search results.
- `--select`: Optional flag to select specific comics to download.

Features:
- Searches for comics on readallcomics.com based on the provided term.
- Displays search results with comic titles.
- Can optionally show URLs for each comic in the search results.
- Provides an option to download all found comics.
- Allows selection of specific comics to download when using the `--select` flag.
- Uses multithreading for faster processing and downloading.
- Skips already downloaded issues to avoid duplicates.
- Sanitizes folder and file names to prevent issues with special characters.
- Creates a folder for each comic series inside a "Comics" directory.
- Saves the source URL in a text file within each comic's folder.

### download_single_issue.py

Downloads a single comic issue from a given URL and saves it as a PDF.

Usage:

```bash
python download_single_issue.py --url <issue_url> --file_path <output_file_path>
```

- `<issue_url>`: The URL of the specific comic issue to download.
- `<output_file_path>`: The file path where the downloaded issue will be saved as a PDF.

Features:
- Fetches images from the provided URL.
- Processes and resizes images for consistent quality.
- Combines all images into a single PDF file.
- Handles both relative and absolute image URLs.
- Uses BeautifulSoup for HTML parsing.
- Utilizes the Pillow library for image processing.
### update_comic.py

Updates the comics library by downloading the latest issues for all comics in the Comics folder.

Usage:

```bash
python update_comic.py
```

Features:
- Scans the Comics folder for all comic subfolders.
- Reads the URL file in each comic subfolder to get the source URL.
- Checks for new issues by comparing available issues with already downloaded ones.
- Downloads new issues using multithreading for improved performance.
- Skips already downloaded issues to avoid duplicates.
- Shows progress bars for both checking updates and downloading new issues.
- Sanitizes file names to prevent issues with special characters.

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
