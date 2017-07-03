import os
from subprocess import call
from shutil import copytree, copy2

def copy_file_or_files_of_dir(src, dst, symlinks=False, ignore=None):
    if os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            else:
                copy2(s, d)
    else:
        copy2(src, dst)

def main(site, logging, conf_id):
    logging.info("Copying files...")

    if not 'copy_files' in site.params:
        logging.error("copy_files action requires a 'copy_files' entry in config.yaml")
        return

    if conf_id:
        conf = site.params['copy_files'][conf_id]
        for src, dest in conf.items():
            if src[0] != "/":
                src = os.path.join(site.base_dir, src)
            if dest[0] != "/":
                dest = os.path.join(site.base_dir, dest)
            try:
                copy_file_or_files_of_dir(src, dest)
            except Exception as e:
                logging.error("Unable to copy {src} to {dest}: {e}".format(src=src, dest=dest, e=e))
    else:
        for conf in site.params['copy_files']:
            for src, dest in conf.items():
                if src[0] != "/":
                    src = os.path.join(site.base_dir, src)
                if dest[0] != "/":
                    dest = os.path.join(site.base_dir, dest)
                try:
                    copy_file_or_files_of_dir(src, dest)
                except Exception as e:
                    logging.error("Unable to copy {src} to {dest}: {e}".format(src=src, dest=dest, e=e))


