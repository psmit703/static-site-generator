# program type:
# JSON -> HTML -> list(HTML)

import json

# replaces all REFs ("$REF-...") in siteData JSON/dict with the actual data from other JSON files
# recursive function
# dict() | list() -> dict() | list() | str()


def replaceREFS(siteData):
    if type(siteData) == dict:
        for key in siteData:
            if type(siteData[key]) == str:
                if siteData[key].startswith("$REF-"):
                    with open(siteData[key][5:], "r") as file:
                        siteData[key] = json.loads(file.read())
                else:
                    siteData[key] = replaceREFS(siteData[key])
            siteData[key] = replaceREFS(siteData[key])
        return siteData
    elif type(siteData) == list:
        for i in range(len(siteData)):
            if type(siteData[i]) == str:
                if siteData[i].startswith("$REF-"):
                    with open(siteData[i][5:], "r") as file:
                        siteData[i] = json.loads(file.read())
                else:
                    siteData[i] = replaceREFS(siteData[i])
            siteData[i] = replaceREFS(siteData[i])
        return siteData
    else:
        return siteData


# void -> void


def main():
    with open("site.json", "r") as file:
        siteJSON = json.loads(file.read())

    replaceREFS(siteJSON)


if __name__ == "__main__":
    main()
