def main(site, logging):
    logging.info("Creating sitemap...")

    pages = site.context['pages']
    print(pages)