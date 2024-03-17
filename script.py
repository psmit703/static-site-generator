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
                    siteData[key] = json.loads(open(siteData[key][5:]).read())
                else:
                    siteData[key] = replaceREFS(siteData[key])
            siteData[key] = replaceREFS(siteData[key])
        return siteData
    elif type(siteData) == list:
        for i in range(len(siteData)):
            if type(siteData[i]) == str:
                if siteData[i].startswith("$REF-"):
                    siteData[i] = json.loads(open(siteData[i][5:]).read())
                else:
                    siteData[i] = replaceREFS(siteData[i])
            siteData[i] = replaceREFS(siteData[i])
        return siteData
    else:
        return siteData


# void -> void


def main():
    siteJSON = json.loads(open("site.json").read())
    replaceREFS(siteJSON)


if __name__ == "__main__":
    main()
