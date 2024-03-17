# Static Site Generator

## Motivation

I have had a portfolio site for a while now, which I built myself. However, it is fairly barebones in terms of technology - while it has a bunch of JavaScript and all that good stuff, it doesn't have a very good way of actually updating files. For example, if I need to update something in the navbar, that has to be done on every page.

This project seeks to solve that in a structured way. By using JSONs (lots and lots of JSONs) to store the site's data and by being given a template HTML file, it will generate the expected HTML files for the entire site.

While this will still require me to actually update the data, it will ensure it is done in a much more consistent way that is significantly less error-prone than if I were to do it manually. It's structure will allow me to easily make both simple updates to individual pages and more complex updates to the entire site's structure.

## JSON Schema

### Full Site

site = {
    "siteName": siteName | "",
    "favicon": relativeDirectory | URL | "",
    "siteWideScripts": [
        {
            "scriptSource": relativeDirectory | URL | "",
            "inLine": "true" | "false",
            "inLineSource": "\$JS-" + (relativeDirectory | URL) | "",
            "scriptType": scriptType | "",
            "defer": "true" | "false",
            "async": "true" | "false",
            "skipPages": [
                String: (name of one of the JSONs inside navbarPages, footerPages, or utilityPages)
            ]
        }
    ],
    "footerDetails": {
        "copyright": {
            "year": year-like string | "",
            "text": copyrightNotice | "",
        },
        "contact": {
            "email": email-like string | "",
        }
    },
    "pageList": {
        "navbarList": [
            String: (name of one of the JSONs inside navbarPages)
        ],
        "footerList": [
            String: (name of one of the JSONs inside footerPages)
        ],
        "utilityList": [
            String: (name of one of the JSONs inside utilityPages)
        ]
    },
    "navbarPages": {
        pageName: {
            "title": pageTitle | "",
            "url": page subdirectory (e.g., "index.html" from "example.com/index.html"),
            "description": pageDescription | "",
            <!-- navWidth is used for custom widths for items in the navbar to maintain uniform centering -->
            "navWidth": "float-like string" | "",
            "overrideFavicon": "true" | "false",
            "pageScripts": [
                {
                    "scriptSource": relativeDirectory | URL | "",
                    "inLine": "true" | "false",
                    "inLineSource": "\$JS-" + (relativeDirectory | URL) | "",
                    "scriptType": "text/javascript",
                    "defer": "true" | "false",
                    "async": "true" | "false"
                }
            ],
            <!-- pageName in the content field should be the same as the pageName that is the name of this JSON -->
            <!-- see section "Individual Page Content" -->
            "content": "\$REF-./navbarPages/pageName.json" | "",
            "type": "sitePage" | "directLink",
            "linkName": linkName for navbar, etc.,
            <!-- skip this page for site generation purposes (useful for preserving the template page) -->
            "skip": "true" | "false"
        }
    },
    "footerPages": {
        pageName: {
            "title": pageTitle | "",
            "url": page subdirectory (e.g., "index.html" from "example.com/index.html"),
            "description": pageDescription | "",
            <!-- navWidth is used for custom widths for items in the navbar to maintain uniform centering -->
            "navWidth": "float-like string" | "",
            "overrideFavicon": "true" | "false",
            "pageScripts": [
                {
                    "scriptSource": relativeDirectory | URL | "",
                    "inLine": "true" | "false",
                    "inLineSource": "\$JS-" + (relativeDirectory | URL) | "",
                    "scriptType": "text/javascript",
                    "defer": "true" | "false",
                    "async": "true" | "false"
                }
            ],
            <!-- pageName in the content field should be the same as the pageName that is the name of this JSON -->
            <!-- see section "Individual Page Content" -->
            "content": "\$REF-./navbarPages/pageName.json" | "",
            "type": "sitePage" | "directLink",
            "linkName": linkName for navbar, etc.,
            <!-- skip this page for site generation purposes (useful for preserving the template page) -->
            "skip": "true" | "false"
        }
    },
    "utilityPages": {
        pageName: {
            "title": pageTitle | "",
            "url": page subdirectory (e.g., "index.html" from "example.com/index.html"),
            "description": pageDescription | "",
            <!-- navWidth is used for custom widths for items in the navbar to maintain uniform centering -->
            "navWidth": "float-like string" | "",
            "overrideFavicon": "true" | "false",
            "pageScripts": [
                {
                    "scriptSource": relativeDirectory | URL | "",
                    "inLine": "true" | "false",
                    "inLineSource": "\$JS-" + (relativeDirectory | URL) | "",
                    "scriptType": "text/javascript",
                    "defer": "true" | "false",
                    "async": "true" | "false"
                }
            ],
            <!-- pageName in the content field should be the same as the pageName that is the name of this JSON -->
            <!-- see section "Individual Page Content" -->
            "content": "$REF-./navbarPages/pageName.json" | "",
            "type": "sitePage" | "directLink",
            "linkName": linkName for navbar, etc.,
            <!-- skip this page for site generation purposes (useful for preserving the template page) -->
            "skip": "true" | "false"
        }
    }
}

### Individual Page Content

<!-- please note that "variables" in this schema with the same name are NOT
necessarily the same variable - discretion should be used as appropriate -->
content = {
    "sections": [
        <!-- each entry in "sections" denotes a vertical portion of the page -->
        <!-- each section is delimited internally by an <hr> element -->
        <!-- delimiters can be individually overridden by specific sections -->
        {
            <!-- each JSON in an individual section denotes horizontal items -->
            <!-- horizontally configured items are not delimited -->
            "overrideTopDelimiter": "false",
            "overrideBottomDelimiter": "false",
            "horizontalItems": [
                {
                    "rawHTML": valid HTML tag | "",
                    "type": "image" | "text" | "markdown" | "card",
                    "classes": string of HTML classes delimited by single spaces | "",
                    "id": HTML id string | "",
                    "title": titleAttribute | "",
                    "altText": altTextAttribute | "",
                    "resourceLink": relativeDirectory | URL | "",
                    "hyperlink": relativeDirector | URL | "",
                    "text": "\$MD-" + relativeDirectoryForMarkdown | text | "",
                    "card": {
                        "title": cardTitle | "",
                        "dates": string date range, enclosed by parentheses | "",
                        <!-- card sections are EXCLUSING the title section and buttons section -->
                        "sections": [
                            {
                                "title": sectionTitle | "",
                                "sectionText": "$MD-" + relativeDirectoryForMarkdown | text | "",
                            }
                        ]
                        "buttons": [
                            {
                                "text": buttonText | "",
                                "hyperlink": buttonLink | ""
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
