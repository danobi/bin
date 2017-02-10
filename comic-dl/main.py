#!/bin/env python3

import argparse
import os

import bs4
import requests

BASE_URL = 'http://www.readcomics.tv/comic/'
DEFAULT_DL_DIR = '.'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102   \
            Safari/537.36'}

def get_issue_urls(overview_url, reverse):
    """Get a list of all the issue urls

    Args:
        overview_url: url of the overview page of the comic
        reverse: boolean flag indicating whether or not to reverse
            the issue download order
    Returns:
        List of urls pointing to the first page of each issue
    """
    res = requests.get(overview_url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    raw_a_tags = soup.find_all('a', class_='ch-name')
    urls = [x['href'] for x in raw_a_tags]
    urls = list(zip(range(1, len(urls)+1), urls)) # Give each url an issue number
    if reverse:
        urls.reverse()
    return urls


def dl_all_issues(comic_name, issue_urls, dl_dir):
    """Download all request issues

    Args:
        comic_name: name of comic we're downloading
        issue_urls: list of urls pointing to the first page of each issue
        dl_dir: directory to put downloaded comic
    Returns:
        None
    """
    # Create directory for this comic
    comic_dir = "{0}/{1}".format(dl_dir, comic_name)
    if not os.path.exists(comic_dir):
        os.makedirs(comic_dir)

    # Download all the issues
    for issue_num,url in issue_urls:
        try:
            issue_dl_dir = "{0}/issue_{1}".format(comic_dir, issue_num)

            # Create download directory for issue
            if not os.path.exists(issue_dl_dir):
                os.makedirs(issue_dl_dir)

            dl_single_issue(issue_num, url, issue_dl_dir)

        except requests.HTTPError as e:
            # This is most likely hit when there's no more pages in an issue
            continue


def dl_single_issue(issue_num, start_url, dl_dir):
    """Downloads a single issue of a comic

    Args:
        issue_num: canonical issue number
        start_url: url pointing to the first page in the issue
        dl_dir: where to put downloaded issue folder
    Returns:
        None
    """
    page = 0

    while True:
        # We increment here so later if the image already exists,
        # we don't have to have weird control flow to increment
        page += 1

        # Grab the entire page
        res = requests.get("{0}/{1}".format(start_url, page))
        res.raise_for_status()

        # Find the image url
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        img_tag = soup.find(id="main_img")
        src = img_tag['src']

        # Download the image
        print("Downloading issue #{0} / page {1}".format(issue_num, page))
        img_path = "{0}/{1}.jpg".format(dl_dir, page)
        if os.path.exists(img_path) and os.path.getsize(img_path):
            print("Page already exists -- skipping")
            continue
        with open(img_path, 'wb') as f:
            res = requests.get(src, headers=HEADERS)
            f.write(res.content)


def main(comic_name, destdir, reverse):
    if destdir:
        dl_dir = destdir
    else:
        dl_dir = DEFAULT_DL_DIR
    overview_url = BASE_URL + comic_name
    issue_urls = get_issue_urls(overview_url, reverse)
    dl_all_issues(comic_name, issue_urls, dl_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download comics')
    parser.add_argument('comic_name', help='Name of comic to download')
    parser.add_argument('-d', '--destdir', help='Destination directory of download')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help="Reverse issue download order. "
                             "This helps to speed up downloding new issues "
                             "to an existing comic folder.")
    args = parser.parse_args()

    main(args.comic_name, args.destdir, args.reverse)
