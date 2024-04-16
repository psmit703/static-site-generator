# Static Site Generator
# JSON -> HTML -> list(HTML)

import json


def replaceREFS(siteData):
    # replaces all REFs ("$REF-...") in siteData JSON/dict with the actual data from other JSON files
    # recursive function

    # NEITHER THIS NOR THE AUXILIARY FUNCTION SUPPORT CIRCULAR REFERENCES
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
    print(json.dumps(siteJSON, indent=4))


if __name__ == "__main__":
    # program entry point

    main()
