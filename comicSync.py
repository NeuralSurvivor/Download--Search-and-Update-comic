
import argparse
from utils import search_and_download, update_comics, download_comic, download_issue
def main():
    parser = argparse.ArgumentParser(description="Comic Sync: Search, download, and update comics.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search and download command
    search_parser = subparsers.add_parser("search", help="Search and download comics")
    search_parser.add_argument("search", help="Search term for comics")
    search_parser.add_argument("--download", "-d", action="store_true", help="Download the comics from search results")
    search_parser.add_argument("--select", "-s", action="store_true", help="Select comics to download")
    search_parser.add_argument("--with-url", "-wu", action="store_true", help="Print result with URL")

    # Update command
    subparsers.add_parser("update", help="Update all comics in the library")

    # Download single comic command
    download_parser = subparsers.add_parser("download", help="Download a single comic or issue")
    download_parser.add_argument("--url", required=True, help="The URL of the comic or issue to download")
    download_parser.add_argument("-f", required=True, help="The folder or file path to save the downloaded comic or issue")
    download_parser.add_argument("-i", "--issue", action="store_true", help="Specify if downloading a single issue")
    args = parser.parse_args()

    if args.command == "search":
        search_and_download(args.search, args.download, args.select, args.with_url)
    elif args.command == "update":
        update_comics()
    elif args.command == "download":
        if args.issue:
            download_issue(args.url, args.f)
        else:
            download_comic(args.url, args.f)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
