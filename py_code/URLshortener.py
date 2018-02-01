import sys
import os
import requests


def shorten(url):
    # prepare url to fetch shotertened url from tiny url
    url = "http://tinyurl.com/api-create.php?url=" + url
    try:
        response = requests.get(url)
        return response.content
    except Exception:
        return "ERROR"

def driver(txt_file, arg_url):
    urls = open(txt_file, "r")
    for idx, url in enumerate(urls):
        idx = idx + 1
        short_url = shorten(url)
        outfile = open("output_urls.txt", "a+")
        outfile.write(str(idx) + ") " + url + "--->" + short_url + "\n")
        outfile.close()

    if (len(arg_url) > 0):
        print"argumented url-", short_url
        short_url = shorten(arg_url)
        print"shortened url-", short_url


if __name__ == "__main__":
    args = sys.argv
    # catch argumented long urls
    try:
        arg_url = args[1]
    except Exception:
        arg_url = []
    # long urls from txt file
    textfile_dir = os.getcwd()
    textifle_name = "url.txt"

    file_location = os.path.join(textfile_dir, textifle_name)

    driver(file_location, arg_url)
    # Pass the url to Shorten method
