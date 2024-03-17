# Static Site Generator
# JSON -> HTML -> list(HTML)

import json


def replaceREFS(siteData):
    # replaces all REFs ("$REF-...") in siteData JSON/dict with the actual data from other JSON files
    # recursive function

    # this has NOT been tested with single-layer references
    # i.e., if a reference itself has another reference, it may not work as expected
    # however this is not something I currently need

    # dict() | list() -> dict() | list() | str()

    if type(siteData) == dict:
        for i in siteData:
            replaceREFSAux(siteData, i)
        return siteData
    elif type(siteData) == list:
        for i in range(len(siteData)):
            replaceREFSAux(siteData, i)
        return siteData
    else:
        return siteData


def replaceREFSAux(siteData, i):
    # handles repetitive pattern previously in replaceREFS()
    # dict() | list() -> int -> void

    if type(siteData[i]) == str:
        if siteData[i].startswith("$REF-"):
            with open(siteData[i][5:], "r") as file:
                siteData[i] = json.loads(file.read())
        else:
            siteData[i] = replaceREFS(siteData[i])
    siteData[i] = replaceREFS(siteData[i])


def main():
    # main function
    # void -> void

    with open("site.json", "r") as file:
        siteJSON = json.loads(file.read())

    replaceREFS(siteJSON)
    print(json.dumps(siteJSON, indent=4))


if __name__ == "__main__":
    # program entry point

    main()
