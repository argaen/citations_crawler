## Description

- Search papers in scopus by author.

Todo:

- Allow to select which fields to return (now Authors, Title, SourceTitle, CitedBy and DOI only).
- Search papers by DOI.
- Search papers in WOK.


## Usage

    usage: main.py [-h] [-s SEARCH] -n NAME -l LAST_NAME [-o]

Search papers by author in scopus or web of science (not working).

    optional arguments:
    -h, --help            show this help message and exit
    -s SEARCH, --search SEARCH
                        Select which db to search (wok|scopus) (default:
                        scopus)
    -n NAME, --name NAME  Name of the author (default: None)
    -l LAST_NAME, --last_name LAST_NAME
                        Last name of the author (default: None)
    -o, --output          Output file (default: False)


## Output

    [ {'field1': 'value1', 'field2': 'value2', ..., 'fieldN': 'valueN'}, ..., {'field1': 'value1', 'field2': 'value2', ..., 'fieldN': 'valueN'} ]
