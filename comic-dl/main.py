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

def get_issue_urls(overview_url):
    res = requests.get(overview_url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    raw_a_tags = soup.find_all('a', class_='ch-name')
    return [x['href'] for x in raw_a_tags]


def dl_all_issues(comic_name, issue_urls, dl_dir):
    # Create directory for this comic
    comic_dir = "{0}/{1}".format(dl_dir, comic_name)
    if not os.path.exists(comic_dir):
        os.makedirs(comic_dir)

    # Download all the issues
    for idx,url in enumerate(issue_urls):
        try:
            issue_dl_dir = "{0}/issue_{1}".format(comic_dir, idx+1)

            # Create download directory for issue
            if not os.path.exists(issue_dl_dir):
                os.makedirs(issue_dl_dir)

            dl_single_issue(idx+1, url, issue_dl_dir)

        except requests.HTTPError as e:
            # This is most likely hit when there's no more pages in an issue
            continue


def dl_single_issue(issue_num, start_url, dl_dir):
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


def main(comic_name, destdir):
    if destdir:
        dl_dir = destdir
    else:
        dl_dir = DEFAULT_DL_DIR
    overview_url = BASE_URL + comic_name
    issue_urls = get_issue_urls(overview_url)
    dl_all_issues(comic_name, issue_urls, dl_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download comics')
    parser.add_argument('comic_name', help='Name of comic to download')
    parser.add_argument('-d', '--destdir', help='Destination directory of download')
    args = parser.parse_args()

    main(args.comic_name, args.destdir)
