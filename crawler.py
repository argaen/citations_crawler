#!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup
import cookielib
import argparse
import csv
import ast
import sys
import requests
from xml.etree import ElementTree

br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)
br.set_handle_robots(False)
br.set_handle_equiv(True)
# br.set_debug_http(True)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def get_orcid_publications_by_author_id(orcid_id):
    res = ['"Authors","Title","Cited by","DOI"']
    r = requests.get("http://pub.orcid.org/%s/orcid-works" % orcid_id)
    ns = {'ns': 'http://www.orcid.org/ns/orcid'}

    root = ElementTree.fromstring(r.text.encode('utf-8'))
    works = root.find('ns:orcid-profile/ns:orcid-activities/ns:orcid-works', ns)

    for work in works.findall('ns:orcid-work', ns):
        title = work.find('ns:work-title', ns).find('ns:title', ns).text

        authors = []
        for e in work.find('ns:work-contributors', ns).findall('ns:contributor', ns):
            authors.append(e.find('ns:credit-name', ns).text.encode('utf-8'))

        if work.find('ns:work-external-identifiers', ns) is not None:
            for e in work.find('ns:work-external-identifiers', ns).findall('ns:work-external-identifier', ns):
                if e.find('ns:work-external-identifier-type', ns).text == 'doi':
                    doi = e.find('ns:work-external-identifier-id', ns).text
        res.append('"' + ",".join(authors) + '","' + title + '","0","' + doi + '"')

    return res


def get_scopus_publications_by_author_id(scopus_id):
    br.open("http://www.scopus.com/authid/detail.url?authorId=%s" % scopus_id)
    br.follow_link(text_regex="View in search results format")

    br.select_form(name="SearchResultsForm")
    br.form.set_all_readonly(False)

    soup = BeautifulSoup(br.response().read())  # Get ALL current EIDs
    br.form["selectedEIDs"] = [x['value'] for x in soup.findAll('input', attrs={'name': 'selectedEIDs'})]

    br.form["oneClickExport"] = '{"Format":"CSV","View":"SpecifyFields", "SelectedFields":"Authors Title SourceTitle CitedBy DOI"}'  # Make selected fields variable?
    br.form["clickedLink"] = "export"
    br.form["selectAllCheckBox"] = ["on"]

    br.submit()

    return br.response()


def get_scopus_publications_by_author(name, last_name):
    br.open("http://www.scopus.com/search/form.url?display=authorLookup&clear=t&origin=searchbasic")

    br.select_form(name="AuthorLookupValidatedSearchForm")

    br.form["searchterm1"] = last_name
    br.form["searchterm2"] = name

    br.submit()

    br.follow_link(text_regex="Documents")

    br.select_form(name="SearchResultsForm")
    br.form.set_all_readonly(False)

    soup = BeautifulSoup(br.response().read())  # Get ALL current EIDs
    br.form["selectedEIDs"] = [x['value'] for x in soup.findAll('input', attrs={'name': 'selectedEIDs'})]

    br.form["oneClickExport"] = '{"Format":"CSV","View":"SpecifyFields", "SelectedFields":"Authors Title SourceTitle CitedBy DOI"}'  # Make selected fields variable?
    br.form["clickedLink"] = "export"
    br.form["selectAllCheckBox"] = ["on"]

    br.submit()

    return br.response()


def get_scopus_publication_by_fields(fields=[]):
    br.open("http://www.scopus.com/search/form.url?display=advanced")

    br.select_form(name="AdvancedValidatedSearchForm")
    br.form.find_control("searchfield").readonly = False

    br.form["searchfield"] = " OR ".join([" " + x[0] + "(" + x[1] + ") " for x in fields])
    br.submit()

    br.select_form(name="SearchResultsForm")
    br.form.set_all_readonly(False)

    soup = BeautifulSoup(br.response().read())  # Get ALL current EIDs
    br.form["selectedEIDs"] = [x['value'] for x in soup.findAll('input', attrs={'name': 'selectedEIDs'})]

    br.form["oneClickExport"] = '{"Format":"CSV","View":"SpecifyFields", "SelectedFields":"Authors Title SourceTitle CitedBy DOI"}'  # Make selected fields variable?
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
    parser = argparse.ArgumentParser(description="Search papers by author in scopus or orcid.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--search', help="Select which db to search (scopus|orcid)", default='scopus')
    parser.add_argument('-o', '--output', help="Output file", action="store_true")

    subparsers = parser.add_subparsers(help='Search by author or article')

    author_parser = subparsers.add_parser('author', help='Search by author name-lastname or scopus_id')
    author_parser.add_argument('-n', '--name', help="Name of the author")
    author_parser.add_argument('-l', '--last_name', help="Last name of the author")
    author_parser.add_argument('-i', '--id', help="Id of the author (scopus_id or orcid_id)")

    article_parser = subparsers.add_parser('article', help='Search by article fields')
    article_parser.add_argument('-a', '--articles', required=True, help="Article fields to look for. Ex: -a '[[DOI, xxxx], [Title, xxxx]]'")

    args = parser.parse_args()

    if args.search == "scopus":
        if "articles" in args:
            print "Method not working."
            sys.exit()
            # res = get_scopus_publication_by_fields(ast.literal_eval(args.articles))
        else:
            if args.name and args.last_name:
                res = get_scopus_publications_by_author(args.name, args.last_name)
            elif args.id:
                res = get_scopus_publications_by_author_id(args.id)
            else:
                print("For author mode, you need to enter either name and last_name or id")
                sys.exit()
    elif args.search == 'orcid':
        if "articles" not in args:
            if args.id:
                res = get_orcid_publications_by_author_id(args.id)
        else:
            print("Only searching by id is supported on orcid.")
            sys.exit()
    else:
        print("Only scopus site is supported right now.")
        sys.exit()

    print(csv_to_dict(csv.reader(res, skipinitialspace=True)))
