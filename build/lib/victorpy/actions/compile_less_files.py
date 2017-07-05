import os
from subprocess import call

def main(site, logging, compiler="lessc"):
    """
    TODO: Doc
    """
    logging.info("Compiling less files using {} compiler...".format(compiler))

    if compiler == "python":
        import lesscpy

    for conf in site.params['less']['files']:
        for src, dest in conf.items():

            if src[0] != "/":
                src = os.path.join(site.base_dir, src)
            if dest[0] != "/":
                dest = os.path.join(site.base_dir, dest)

            if compiler == "lesscpy":
                os.chdir(os.path.dirname(src))

                css_content = lesscpy.compile(src, minify=True, xminify=True)

                dest_dir = os.path.dirname(dest)

                if not os.path.exists(dest_dir):
                    logging.info("Dest dir not exist, creating...")
                    os.makedirs(dest_dir)

                with open(dest, 'w') as f:
                    f.write(css_content)

            elif compiler == "lessc":
                call(["lessc", "--clean-css", src, dest])
