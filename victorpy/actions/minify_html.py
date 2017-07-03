import htmlmin
import os

def main(site, logging):
    logging.info("Minifying outputed HTML files...")

    for root, dirs, files in os.walk(site.build_path):
        for file in files:
            try:
                extension = os.path.splitext(file)[1]
                if extension == ".html":
                    absolute_path = os.path.join(root, file)
                    f = open(absolute_path, 'r')
                    content = f.read()
                    f.close()

                    with open(absolute_path, 'w') as f:
                        f.write(htmlmin.minify(content))
            except Exception as e:
                logging.warning("Unable to load file {file}: {e}".format(file=file, e=e))

