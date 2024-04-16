# Static Site Generator
# JSON -> HTML -> list(HTML)

import json


def replaceREFS(siteData):
    # replaces all REFs ("$REF-...") in siteData JSON/dict with the actual data from other JSON files
    # recursive function

    # NEITHER THIS FUNCTION NOR replaceREFSAux() SUPPORT CIRCULAR REFERENCES
    # I haven't tested this with circular references, but I believe it will result in an infinite loop
    # just don't do that
    # please
    # please do not use circular references
    # :D

    # dict() | list() -> dict() | list() | str()

    if type(siteData) == dict:
        for i in siteData:
            replaceREFSAux(siteData, i)
    elif type(siteData) == list:
        for i in range(len(siteData)):
            replaceREFSAux(siteData, i)

    return siteData


def replaceREFSAux(siteData, i):
    # handles repetitive pattern previously in replaceREFS()
    # dict() | list() -> int -> void

    if type(siteData[i]) == str:
        if siteData[i].startswith("$REF-"):
            with open(siteData[i][5:], "r") as file:
                siteData[i] = replaceREFS(json.loads(file.read()))
        else:
            siteData[i] = replaceREFS(siteData[i])
    siteData[i] = replaceREFS(siteData[i])


def main():
    # main function
    # void -> void

    with open("site.json", "r") as file:
        siteJSON = json.loads(file.read())

    replaceREFS(siteJSON)

    # load all page names and their respective sections
    pages = {}
    for section in siteJSON["pageList"]:
        for page in siteJSON["pageList"][section]:
            pages[page] = section

    # load and process data for each page
    # pages[page] = section
    for page in pages:
        section = "navbarPages" if pages[page] == "navbarList" \
            else "footerPages" if pages[page] == "footerList" \
            else "utilityPages" if pages[page] == "utilityList" \
            else "INVALID SECTION"

        pageData = siteJSON[section][page]

        print(pageData)

    print(json.dumps(siteJSON, indent=4))


if __name__ == "__main__":
    # program entry point

    main()
