## Description

- Return papers in scopus by author or scopus id.
- Return papers in scopus by article field.
- Return papers in orcid by author id.

Todo:

- Allow to select which fields to return (now Authors, Title, SourceTitle, CitedBy and DOI only).
- Search papers in WOK.
- Narrow the authors search (similar names)
- Allow complex queries for papers like Title=title AND Author=Mr.X


## Installation

You need to install mechanize and beautifulsoup4:

     pip install mechanize beautifulsoup4


## Usage

### General

    usage: crawler.py [-h] [-s SEARCH] [-o] {author,article} ...

    Search papers by author in scopus or orcid.

    positional arguments:
      {author,article}      Search by author or article
        author              Search by author name-lastname
        article             Search by article fields

    optional arguments:
      -h, --help            show this help message and exit
      -s SEARCH, --search SEARCH
                            Select which db to search (scopus) (default:
                            scopus)
      -o, --output          Output file (default: False)


### By Author

    usage: crawler.py author [-h] -n NAME -l LAST_NAME

    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  Name of the author
      -l LAST_NAME, --last_name LAST_NAME
                            Last name of the author
      -i SCOPUS_ID, --scopus_id SCOPUS_ID Scopus if of the author

- *Example*: python crawler.py author -n john -l doe
- *Example*: python crawler.py author -i 6602739976
- *Example*: python crawler.py -s orcid author -i 0000-0002-3597-4310

### By Article Field (needs rewrite, not working since scopus changed html structure)

    usage: crawler.py article [-h] -a ARTICLES

    optional arguments:
      -h, --help            show this help message and exit
      -a ARTICLES, --articles ARTICLES
                            Article fields to look for. Ex: -a '[[DOI, xxxx],
                            [Title, xxxx]]'

- *Example*: python crawler.py article -a '[["Title", "My paper is ****** awesome"], ["DOI", "xxxxxxxx"]]'

## Output

    [ {'field1': 'value1', 'field2': 'value2', ..., 'fieldN': 'valueN'}, ..., {'field1': 'value1', 'field2': 'value2', ..., 'fieldN': 'valueN'} ]
