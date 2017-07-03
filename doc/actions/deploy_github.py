import os
from subprocess import call
from time import gmtime, strftime

def main(site, logging):
    logging.info("Preparing for github...")

    command = 'git init && git remote add origin https://github.com/pascallando/pascallando.github.io.git && git add . && git commit -m "{}" && git push -f origin master'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    logging.info(command)
    os.chdir(site.build_dir)
    call(command, shell=True)
    os.chdir(site.base_dir)

