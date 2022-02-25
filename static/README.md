# Static webpage files

JavaScript and CSS files

## General

This package and the simulation uses [bootstrap 5.1.3][ref-bootstrap]

## Create compressed version

### Why

To speed up the data transfer between the device and a browser, many of them
accept CSS and JS files as compressed `.gz` files.

### Additional informations

In some cases the following warning can be seen in the web console of the page

	Layout rendering was forced before the page was fully loaded.

This might be due to the reason of loading multiple (CSS) files within a given
time frame. As a less powerfull device, such as an ESP32 or ESP8266, will have
difficulties to provide these data in the expected time frame, the layout
rendering might be forced, leading to a not as expected view.

To avoid such issues, try to serve as less files as possible in the most
compact way. To do so, use minified versions of CSS files (`*.min.css`) and
combine multiple files into one. An even better performance is reached by
compressing the file as shown onwards.

To minify custom CSS files, search online for a CSS minifier or use
[this one][ref-css-minifier]

### How to

To compress a file use `gzip` instead of `tar`. `tar` seems to break something
in the compressed file. As a result the style might not be as with the non
compressed version.

This example shows how to compress `bootstrap.min.css` to a new file called
`bootstrap.min.css.gz`

```bash
cd css

gzip -r bootstrap.min.css -c > bootstrap.min.css.gz
```

<!--
### How to

Combine the as of now two custom CSS files (`list-groups.css` and `style.css`)
into one file (`combined.css`)

```bash
cd css

cat list-groups.css style.css > combined.css
```

Minify the generated file with a CSS minifier e.g. [this one][ref-css-minifier]
into a file named `combined.min.css` inside the [css folder](`css`)

Append the minified content to the `bootstrap.min.css` file after removing the
`/*# sourceMappingURL=bootstrap.min.css.map */` string from the file, see
[Stackoverflow Delete specific string from text file][ref-stackoverflow-sed]

```bash
cd css

sed 's?\/\*\# sourceMappingURL=bootstrap.min.css.map \*/??' ./bootstrap.min.css > bootstrap_extended.min.css
cat combined.min.css >> bootstrap_extended.min.css
```

Open the `bootstrap_extended.min.css` file and remove any empty lines before
the attached content of `combined.min.css`

Finally compress the extended bootstrap file

```bash
cd css

tar -czf bootstrap_extended.min.css.gz bootstrap_extended.min.css
```

Or use the [provided script](compress_static_files.sh) to perform all these
steps at once and follow the instructions on the terminal

```bash
sh create_single_css_file.sh
```
-->

<!-- Links -->
[ref-bootstrap]: https://getbootstrap.com/docs/5.1/getting-started/download/
[ref-css-minifier]: https://www.toptal.com/developers/cssminifier/
[ref-stackoverflow-sed]: https://stackoverflow.com/questions/5410757/how-to-delete-from-a-text-file-all-lines-that-contain-a-specific-string
