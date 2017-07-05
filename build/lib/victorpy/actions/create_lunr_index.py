import json
import os

def main(site, logging):
    logging.info("Generating lunr index in {}...".format(site.static_dir))

    data = [{
        'title': p.params['title'],
        'description': p.params['description'],
        'keywords': p.params['keywords'],
        'tags': p.tags,
        'href': p.url,
        'content': p.markdown
    } for p in site.pages_list]

    if not os.path.exists(site.static_dir):
        logging.info("Static dir not exist, creating...")
        os.makedirs(site.static_dir)

    target_path = os.path.join(site.static_dir, "index.json")

    with open(target_path, 'w') as f:
        json.dump(data, f)

