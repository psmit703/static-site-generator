# Static Site Generator
# JSON -> HTML -> list(HTML)

import json
import markdown as md


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

    # generate navbar
    template = generateNavBar(template, pageData, siteData)

    # generate body
    template = generateBody(template, pageData, siteData)

    # generate footer
    template = template.replace(
        "$REF-Copyright", siteData['footerDetails']['copyright']['year'] + " " + siteData['footerDetails']['copyright']['text'])
    template = template.replace(
        "$REF-Contact", siteData['footerDetails']['contact']['email'])

    with open(f"./siteFiles/{pageData['url']}", "w") as file:
        file.write(template)


def generateNavBar(template, pageData, siteData):
    raise NotImplementedError("genNavBar() not implemented yet")


def generateBody(template, pageData, siteData):
    # TODO: test
    # String -> JSON -> JSON -> String
    # outputs the edited template input
    # replaces $REF-Body with the actual body for the page

    if len(pageData['content']['sections']) == 0:
        # skip rest of function if no sections
        return template.replace("$REF-Body", "")

    vertSections = []
    for section in pageData['content']['sections']:
        # generate HTML for each vertical section of a page
        vertSections.append((generateVertSection(section, pageData, siteData),
                             section['overrideTopDelimiter'], section['overrideBottomDelimiter']))

    htmlList = []
    i = 0
    while i < len(vertSections):
        # handles horizontal rules between sections
        # processes overrideTopDelimiter and overrideBottomDelimiter
        if i != 0 and vertSections[i][1] == "true":
            if htmlList[-1] == "<hr />":
                htmlList.pop()

        htmlList.append(vertSections[i][0])

        if i != len(vertSections) - 1 and vertSections[i][2] == "false":
            # if the next section overrides its top delimiter, this will be removed
            # in the next iteration in the first if statement of this while loop
            htmlList.append("<hr />")

    return template.replace("$REF-Body", "".join(htmlList))


def generateVertSection(sectionData, pageData, siteData):
    # TODO: test
    # JSON -> JSON -> JSON -> String
    # generates the HTML for a vertical section of a page

    if len(sectionData['horizontalItems']) == 0:
        return ""

    horizontalSections = []
    for section in sectionData['horizontalItems']:
        # generate HTML for each horizontal section of a vertical section
        horizontalSections.append(generateHorizSection(
            section, pageData, siteData))

    if len(horizontalSections) > 1:
        # handles multiple horizontal sections
        # i.e., needs a row system
        if len(horizontalSections) > 3:
            # case for four or more horizontal sections
            # uses col-sm
            i = 0
            while i < len(horizontalSections):
                if horizontalSections[i].startsWith("<div class=\""):
                    horizontalSections[i] = horizontalSections[i][0:12] + "col-sm " + \
                        horizontalSections[i][12:]
                else:
                    horizontalSections[i] = horizontalSections[i][0:4] + " class=\"col-sm\" " + \
                        horizontalSections[i][4:]
                i += 1
        else:
            # case for three or fewer horizontal sections
            # uses col-md
            i = 0
            while i < len(horizontalSections):
                if horizontalSections[i].startsWith("<div class=\""):
                    horizontalSections[i] = horizontalSections[i][0:12] + "col-md " + \
                        horizontalSections[i][12:]
                else:
                    # assumes it starts with "<div" and has no classes
                    horizontalSections[i] = horizontalSections[i][0:4] + " class=\"col-md\" " + \
                        horizontalSections[i][4:]
                i += 1

        row = "\n".join(horizontalSections)
        if sectionData['htmlClasses'] != "":
            # adds custom classes in addition to the default "row" class
            row = f"<div class=\"row {sectionData['htmlClasses']}\">\n" + \
                row + "\n</div>"
        else:
            row = "<div class=\"row\">\n" + row + "\n</div>"

        title = ""
        if sectionData['title'] != "" and sectionData['titleId'] != "":
            # adds a title to the vertical section
            title = f"<h4 id={sectionData['titleId']} class=\"text-center\">{sectionData['title']}</h4>\n"
        elif sectionData['title'] != "":
            title = f"<h4 class=\"text-center\">{sectionData['title']}</h4>\n"

        notes = ""
        if sectionData['notes'] != "":
            # adds notes to the vertical section
            notes = f"<h5 class=\"text-center\"><i>{sectionData['notes']}</i></h5>\n"

        return title + notes + row

    else:
        # case for only one horizontal section
        # i.e., no need for a row
        return horizontalSections[0]


def generateHorizSection(sectionData, pageData, siteData):
    # JSON -> JSON -> JSON -> String
    # generates the HTML for a horizontal section of a vertical section of a page

    match type:
        case "image":
            divId = f"id={sectionData['id']}" if sectionData['id'] != "" else ""
            divClass = f"class=\"{sectionData['classes']}\"" if sectionData['classes'] != "" else ""
            imgTitle = f"title=\"{sectionData['title']}\"" if sectionData['title'] != "" else ""
            imgAlt = f"alt=\"{sectionData['alt']}\"" if sectionData['alt'] != "" else ""
            src = f"src=\"{sectionData['resourceLink']}\""
            href = f"href=\"{sectionData['hyperlink']}\"" if sectionData['hyperlink'] == "true" else ""
            subClass = f"class=\"{sectionData['subClasses']}\"" if sectionData['subClasses'] != "" else ""
            subId = f"id={sectionData['subId']}" if sectionData['subId'] != "" else ""
            styles = f"style=\"{sectionData['styles']}\"" if sectionData['styles'] != "" else ""
            subStyles = f"style=\"{sectionData['subStyles']}\"" if sectionData['subStyles'] != "" else ""

            return f"<div {divId} {divClass} {styles}>\n" + \
                   (f"<a {href}>\n" if href != "" else "") + \
                   f"<img {imgTitle} {imgAlt} {src} {subId} {subClass} {subStyles}>\n" + \
                   (f"</a>\n" if href != "" else "") + \
                   "</div>"
        case "text":
            raise NotImplementedError("genHorizSection() not implemented yet")
        case "markdown":
            html = md.markdown(sectionData['markdown'])
            divId = f"id={sectionData['id']}" if sectionData['id'] != "" else ""
            divClass = f"class=\"{sectionData['classes']}\"" if sectionData['classes'] != "" else ""
            href = f"href=\"{sectionData['hyperlink']}\"" if sectionData['hyperlink'] == "true" else ""
            subClass = f"class=\"{sectionData['subClasses']}\"" if sectionData['subClasses'] != "" else ""
            subId = f"id={sectionData['subId']}" if sectionData['subId'] != "" else ""
            styles = f"style=\"{sectionData['styles']}\"" if sectionData['styles'] != "" else ""
            subStyles = f"style=\"{sectionData['subStyles']}\"" if sectionData['subStyles'] != "" else ""
            title = f"<h4 class=\"text-center\">{sectionData['title']}</h4>\n" if sectionData['title'] != "" else ""

            elmtsList = html.split("\n")
            i = 0
            while i < len(elmtsList):
                elmtsList[i] = addAttrs(
                    elmtsList[i], subClass, subId, subStyles)
                i += 1
            html = "".join(elmtsList)

            return f"<div {divId} {divClass} {styles}>" + \
                (f"<a {href}>\n" if href != "" else "") + \
                title + html + \
                (f"</a>\n" if href != "" else "") + \
                "</div>"
        case "card":
            raise NotImplementedError("genHorizSection() not implemented yet")
        case "rawHTML":
            return sectionData['rawHTML']
        case _:
            raise ValueError(
                f"Invalid horizontal section type\n\nPage Data:\n{pageData}\n\nSection Data:\n{sectionData}")

    raise NotImplementedError("genHorizSection() not implemented yet")


def addAttrs(html, classes, id, styles):
    # String -> String
    # adds classes and ids to HTML elements
    # returns the edited HTML
    # for these purposes, only does it for div, ul, and p

    if html.startswith("<div") or html.startswith("<ul") or html.startswith("<p"):
        endTag = html.find(">") + 1
        tag = html[0:endTag]
        innerStuff = tag.split(" ")
        innerStuff.append(f"id=\"{id}\"")
        innerStuff.append(f"class=\"{classes}\"")
        innerStuff.append(f"style=\"{styles}\"")
        tag = " ".join(innerStuff)
        return tag + html[endTag:]

    return html


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
        if siteData[i].startswith("$JSON-"):
            # handles references to other JSON files
            with open(siteData[i][6:], "r") as file:
                siteData[i] = replaceREFS(json.loads(file.read()))
        elif siteData[i].startswith("$MD-") or siteData[i].startswith("$JS-"):
            # TODO: test
            # handles references to markdown or JavaScript files
            with open(siteData[i][4:], "r") as file:
                siteData[i] = file.read()
        elif siteData[i].startswith("$HTML-"):
            # TODO: test
            # handles references to HTML files
            with open(siteData[i][7:], "r") as file:
                siteData[i] = file.read()
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
