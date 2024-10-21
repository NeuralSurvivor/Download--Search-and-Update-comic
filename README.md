# ComicSync

ComicSync is a Python-based tool for searching, downloading, and updating comics from readallcomics.com.

## Features

- Search for comics
- Download comics
- Update existing comics with new issues
- Download single comics or issues

## Installation

1. Clone the repository:
   ```besh
   git clone https://github.com/yourusername/ComicSync.git
   cd ComicSync
   ```
   

3. Install the required dependencies:
   ```besh
   pip install -r requirements.txt
   ```

## Usage

ComicSync provides several commands:

### Search and Download

Search for comics and optionally download them:

```besh
python comicSync.py search <search_term> [--download] [--select] [--with-url]
```

- `<search_term>`: The term to search for
- `--download` or `-d`: Download the comics from search results
- `--select` or `-s`: Select specific comics to download
- `--with-url` or `-wu`: Display URLs in search results

### Update Comics

Update all comics in your library with new issues:

```besh
python comicSync.py update
```

### Download Single Comic or Issue

Download a specific comic or issue:

```besh
python comicSync.py download --url <url> -f <folder_or_file_path> [--issue]
```

- `--url`: The URL of the comic or issue to download
- `-f`: The folder or file path to save the downloaded comic or issue
- `--issue` or `-i`: Specify if downloading a single issue

## File Structure

- `comicSync.py`: Main script with command-line interface
- `utils.py`: Utility functions for searching, downloading, and updating comics
- `download_single_issue.py`: Script for downloading individual comic issues

## Dependencies

- requests
- beautifulsoup4
- tqdm
- simple-term-menu

## License

[MIT License](LICENSE)

## Disclaimer

This tool is for educational purposes only. Please respect copyright laws and support comic creators by purchasing their work when possible.
