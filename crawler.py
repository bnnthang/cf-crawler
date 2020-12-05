#!/usr/bin/env python3


import json
import os
import re
import requests
import sys
import time
from bs4 import BeautifulSoup


extension_dict = dict()
verdict_dict = dict()

acceptedOnly = False
AC_MSG = "Accepted"


class NotAcceptedError(Exception):
    pass


def load_dicts():
    global extension_dict
    global verdict_dict
    with open("lang.json") as file:
        extension_dict = json.load(file)
    with open("verdict.json") as file:
        verdict_dict = json.load(file)


def shorten_verdict(verdict):
    for key in verdict_dict:
        if key in verdict:
            return verdict_dict[key]


def send_request(url):
    request = requests.get(url)
    # delay 0.3s for each request
    time.sleep(0.3)
    return BeautifulSoup(request.text, "html.parser")


def get_codefile(submission_url):
    """
    Scrape the code file from a given URL

    Args:
    - submission_url: the URL to the submission
    """
    global extension_dict
    global acceptedOnly
    soup = send_request(submission_url)
    try:
        print(f"Crawling {submission_url}")
        # get the code base
        codebase = soup.find("pre", id="program-source-text").text
        codelines = codebase.split("\r\n")
        # get some details
        general_info = list(soup.find("tr").find_next_sibling().children)
        problem_code = general_info[5].find("a").text.strip()
        lang = general_info[7].text.strip()
        verdict = general_info[9].text.strip()
        submitted_time = general_info[15].text.strip().replace(":", "-")
        # check accepted only
        if acceptedOnly and verdict != AC_MSG:
            raise NotAcceptedError
        # set filename
        filename = f"[{problem_code}][{shorten_verdict(verdict)}][{submitted_time}].{extension_dict[lang]}"
        # write to file
        with open(filename, "w+") as dest:
            for line in codelines:
                dest.write(line)
                dest.write("\n")
    except NotAcceptedError:
        print("This is not an AC submission.")
    except:
        print("Error occurred. Skipped.")
    else:
        print("Completed.")


def scrape_page(page_url):
    soup = send_request(page_url)
    submission_table = list(soup.find("table", "status-frame-datatable").children)[2:]
    for i in range(len(submission_table)):
        try:
            if i % 2 == 0:
                continue
            details = list(submission_table[i].children)
            submission_id = str(details[1].text).strip()
            problem_url = str(details[7].find("a")["href"])
            submission_url = "https://codeforces.com" + re.match("/contest/\d+", problem_url)[0] + "/submission/" + submission_id
            get_codefile(submission_url)
        except:
            pass


if __name__ == "__main__":
    load_dicts()
    handles = sys.argv[1:]
    if handles[0] == "-ac":
        handles = handles[1:]
        acceptedOnly = True
    for handle in handles:
        # get number of pages
        try:
            soup = send_request(f"https://codeforces.com/submissions/{handle}")
            pages = int(soup.find_all("span", "page-index")[-1]["pageindex"])
        except IndexError:
            pages = 1
        # create new folder
        if not os.path.isdir(handle):
            os.mkdir(handle)
        # move to a subfolder
        os.chdir(handle)
        # crawl
        for i in range(1, pages + 1):
            scrape_page(f"https://codeforces.com/submissions/{handle}/page/{i}")
        # go back
        os.chdir("..")