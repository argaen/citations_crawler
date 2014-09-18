#!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup
import cookielib
import argparse
import csv

br = mechanize.Browser()
cookiejar =cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)
br.set_handle_robots(False)
br.set_handle_equiv(True)
# br.set_debug_http(True)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def search_wok_by_author(name, last_name): # Under development

    br.open("http://sauwok5.fecyt.es/apps/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=1EFddcK3PdeMNOGGMCM&preferencesSaved=&highlighted_tab=WOS");

    br.select_form(name='accesoSistemaDir');

    br.submit();

    br.follow_link(url="http://sauwok5.fecyt.es/www/?DestApp=WOS")

    br.select_form(name="WOS_GeneralSearch_input_form");

    br.form["value(input1)"] = "GUIMERA R"
    br.form["value(select1)"] = ["AU"]

    br.submit();

    br.follow_link(text="Create Citation Report")

    soup = BeautifulSoup(br.response().read())

    num_results = soup.find("span", {"id": "RESULTS_FOUND"})

    return br.response()


def search_scopus_by_author(name, last_name):

    br.open("http://www.scopus.com/search/form.url?display=authorLookup&clear=t&origin=searchbasic")

    br.select_form(name="AuthorLookupValidatedSearchForm")

    br.form["searchterm1"] = last_name
    br.form["searchterm2"] = name

    br.submit()

    br.follow_link(text_regex="Documents")

    br.select_form(name="SearchResultsForm")
    br.form.set_all_readonly(False)

    soup = BeautifulSoup(br.response().read())  #Get ALL current EIDs
    br.form["selectedEIDs"] = [ x['value'] for x in soup.findAll('input', attrs={'name': 'selectedEIDs'}) ]

    br.form["oneClickExport"] = '{"Format":"CSV","View":"SpecifyFields", "SelectedFields":"Authors Title SourceTitle CitedBy DOI"}' #Make selected fields variable?
    br.form["clickedLink"] = "export"
    br.form["selectAllCheckBox"] = ["on"]

    br.submit()

    return br.response()


def csv_to_dict(data):
    keys = e = []

    for i, r in enumerate(data):
        if i == 0:
            keys = ','.join(r).decode("utf-8-sig").encode("utf-8").split(',')
        else:
            e.append(dict(zip(keys, r)))

    return e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search papers by author in scopus or web of science (not working).", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--search', help = "Select which db to search (wok|scopus)", default = 'scopus')
    parser.add_argument('-n', '--name', required = True, help = "Name of the author")
    parser.add_argument('-l', '--last_name', required = True, help = "Last name of the author")
    parser.add_argument('-o', '--output', help = "Output file", action = "store_true")

    args = parser.parse_args()

    if args.search == "wok":
        res = search_wok_by_author(args.name, args.last_name)
    else:
        res = search_scopus_by_author(args.name, args.last_name)

    print csv_to_dict(csv.reader(res, skipinitialspace=True))

