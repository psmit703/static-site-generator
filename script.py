# Static Site Generator
# JSON -> HTML -> list(HTML)

import json


def generatePage(pageData, siteData, section):
    # JSON -> JSON -> String -> void
    # generates the HTML for a page
    # writes to file
    # no return type, but may throw an error if invalid page section type

    if section == "INVALID SECTION":
        raise ValueError(f"Invalid section type:\n{section}\n{pageData}")

    if pageData['skip'] == "true":
        return

    with open("./siteFiles/template.html", "r") as file:
        template = file.read()

    # generate head elements
    template = template.replace(
        "$REF-Title", f"{pageData['title']} | {siteData['siteName']}")
    template = template.replace("$REF-Favicon", siteData['favicon'])
    template = template.replace("$REF-Description", pageData['description'])
    template = template.replace("$REF-Author", siteData['author'])

    if pageData['title'] == "Home":
        template = template.replace("$REF-Canonical", siteData['url'])
    else:
        template = template.replace(
            "$REF-Canonical", siteData['url'] + pageData['url'])
    template = replaceStylesheets(template, pageData, siteData)
    template = replaceScripts(template, pageData, siteData)

    # generate body
    template = generateBody(template, pageData, siteData)

    # generate footer
    template = template.replace(
        "$REF-Copyright", siteData['footerDetails']['copyright']['year'] + " " + siteData['footerDetails']['copyright']['text'])
    template = template.replace(
        "$REF-Contact", siteData['footerDetails']['contact']['email'])

    with open(f"./siteFiles/{pageData['url']}", "w") as file:
        file.write(template)


def genreteBody(template, pageData, siteData):
    # String -> JSON -> JSON -> String
    # outputs the edited template input
    # replaces $REF-Body with the actual body for the page
    raise NotImplementedError("generateBody() not implemented yet")


def replaceScripts(template, pageData, siteData):
    # String -> JSON -> JSON -> String
    # outputs the edited template input
    # replaces $REF-Scripts with the actual scripts for the page
    scripts = ""

    for data in [siteData, pageData]:
        for each in data['siteWideScripts']:
            if pageData['title'] in each['skipPages']:
                continue

            attrs = ""
            for note in each['notes']:
                if each['notes'][note] == "":
                    attrs += f" {note}"
                else:
                    attrs += f""" {note}=\"{each['notes'][note]}\""""
            attrs = attrs.strip()

            code = ""
            if each['inLine'] == "true":
                with open(each["inLineSource"][4:], "r") as file:
                    code = file.read()
                scripts += f"<script {attrs}>\n{code}\n</script>\n"
            else:
                scripts += f"<script src=\"{each['scriptSource']}\" {attrs}></script>\n"

    return template.replace("$REF-Scripts", scripts)


def replaceStylesheets(template, pageData, siteData):
    # String -> JSON -> JSON -> String
    # outputs the edited template input
    # replaces $REF-Stylesheets with the actual stylesheets for the page
    styles = ""

    for data in [siteData, pageData]:
        for each in data['siteWideStylesheets']:
            if pageData['title'] in each['skipPages']:
                continue

            attrs = ""
            for note in each['notes']:
                if each['notes'][note] == "":
                    attrs += f" {note}"
                else:
                    attrs += f""" {note}=\"{each['notes'][note]}\""""
            attrs = attrs.strip()

            styles += f"<link rel=\"stylesheet\" href=\"{each['styleSource']}\" {attrs}>\n"

    return template.replace("$REF-Stylesheets", styles)


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

    # replaceREFS(siteJSON)

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

        generatePage(pageData, siteJSON, section)

    # print(json.dumps(siteJSON, indent=4))


if __name__ == "__main__":
    # program entry point

    main()
