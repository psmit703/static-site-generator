# Static Site Generator

## Motivation

I have had a portfolio site for a while now, which I built myself. However, it is fairly barebones in terms of technology - while it has a bunch of JavaScript and all that good stuff, it doesn't have a very good way of actually updating files. For example, if I need to update something in the navbar, that has to be done on every page.

This project seeks to solve that in a structured way. By using JSONs (lots and lots of JSONs) to store the site's data and by being given a template HTML file, it will generate the expected HTML files for the entire site.

While this will still require me to actually update the data, it will ensure it is done in a much more consistent way that is significantly less error-prone than if I were to do it manually. It's structure will allow me to easily make both simple updates to individual pages and more complex updates to the entire site's structure.
