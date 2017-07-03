import os
from subprocess import call

def main(site, logging):
    logging.info("Transcrypt'ing Python to JS...")

    current_dir = os.getcwd()

    os.chdir(os.path.join(site.base_dir, "app"))
    call(["transcrypt", "main.py", "-n"])

    os.chdir(current_dir)
