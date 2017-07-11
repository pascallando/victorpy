#!/usr/bin/env python3
from victorpy.__init__ import __version__
from enum import Enum
from collections import OrderedDict
from operator import itemgetter
import os
import shutil
import re
import json
import argparse
import sys
import hashlib
from datetime import datetime, date
from subprocess import call

import jinja2
from flask import Flask, abort, redirect
from slugify import UniqueSlugify
from yaml import load as load_yaml
try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader

import logging
logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)
logging.addLevelName(logging.INFO, "\033[1;02m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName(logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

# ----------------------------
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer, escape=False)
# ----------------------------

def load_module(path, module_name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module


class PageType(Enum):
    CONTENT = 1
    TAG = 2
    OTHER = 99

class Page(object):
    def __init__(self, path, raw_content, site, page_type=PageType.CONTENT, template="page.html"):
        self.path = path
        self.site = site
        self.absolute_path = os.path.join(site.content_dir, path[1:])
        self.build_dir = site.build_dir
        self.raw_content = raw_content
        self.base_dir = site.base_dir
        self.template = template
        self.page_type = page_type
        self.params = {
            'title': None,
            'short_title': None,
            'long_title': None,
            'shortest_title': None,
            'longest_title': None,
            'description': None,
            'keywords': None,
            'template': template,
            'tags': [],
            'draft': False,
            'date': "TODO",
            'position': 0,
        }

        self.unique_id = hashlib.md5(self.path.encode('utf-8')).hexdigest()
        self.slug = os.path.splitext(os.path.basename(path))[0]

        if self.slug == "index":
            self.url = os.path.dirname(self.path)
        else:
            self.url = os.path.join(os.path.dirname(self.path), self.slug)

        if self.url[-1] != "/":
            self.url += "/"

        self.section_url = os.path.split(self.path)[0]
        if self.section_url[-1] == "/":
            self.section_url, self.direct_section_slug, self.parent_section_url = None, None, None
        else:
            self.parent_section_url = os.path.split(self.section_url)[0]
            if self.parent_section_url[-1] == "/" or self.parent_section_url == self.section_url:
                self.parent_section_url = None
            else:
                self.parent_section_url += "/"

            self.section_url += "/"
            self.direct_section_slug = self.section_url.split(os.sep)[-2]

        self.permalink = os.path.join(site.params['base_url'], self.url[1:])

        self.relative_path = self.path
        if self.relative_path.startswith("/"):
            self.relative_path = self.relative_path[1:]

        if self.slug != "index":
            self.dest_path = os.path.join(self.build_dir, os.path.dirname(self.relative_path), self.slug, "index.html")
        else:
            self.dest_path = os.path.join(self.build_dir, os.path.dirname(self.relative_path), "index.html")


        if self.direct_section_slug and self.slug == "index":
            self.is_section_index = True
        else:
            self.is_section_index = False

        self.context = {}
        self.mini_context = {}
        self.front_matter = None
        self.markdown = None
        self.html = ""
        self.toc = None
        self.full_content = None
        self.section_page = None
        self.section_pages = []
        self.section_sections = []
        self.sub_sections = []
        self.breadcrumb = []
        self.tags = []

    def _extract_content(self):
        pattern = re.compile(r'(---)(.*?)(---)(.*)', re.DOTALL)
        parts = re.split(pattern, self.raw_content)
        try:
            self.front_matter = parts[2]
            self.markdown = parts[4]
        except:
            pass

    def _process_front_matter_content(self):
        front_matter_params = load_yaml(self.front_matter, Loader=YamlLoader)
        self.params = {**self.params, **front_matter_params}

    def _process_markdown_content(self):
        # self.html = markdown2.markdown(self.markdown, extras=['header-ids', 'toc', 'fenced-code-blocks', 'tables', 'footnotes'])
        self.html = markdown(self.markdown)

    def process_file_content(self):
        self._extract_content()
        self._process_front_matter_content()
        self._process_markdown_content()

    def process_shortcodes(self):
        def callback(g):
            shortcode_string = g.group(1)
            elements = re.findall(r'(?:[^\s"]|"(?:\\.|[^"])*")+', shortcode_string)
            shortcode = elements[0]
            all_args = elements[1:]
            args = [self.context] + [e for e in all_args if "=" not in e]
            kwargs_list = [e.split("=") for e in all_args if "=" in e]
            kwargs = {e[0]: e[1].replace('"', '') for e in kwargs_list}
            try:
                func = getattr(user_shortcodes, shortcode)
            except:
                func = getattr(default_shortcodes, shortcode)
            return func(*args, **kwargs)

        try:
            # Preserve <code></code>
            pattern = re.compile(r'<pre>(.*?)</pre>', re.MULTILINE|re.DOTALL)
            quotes = re.finditer(pattern, self.html)
            self.html = re.sub(pattern, r'_PRE_', self.html)
            # -------------------------

            regex = re.compile(r"\{\%\s*(.*?)\s*\%\}", re.MULTILINE)
            self.html = regex.sub(callback, self.html)
        except Exception as e:
            logging.warning("Unable to process shortcode for {page}: {e}".format(page=self.url, e=e))
        finally:
            # Restore <code></code>
            for quote in quotes:
                self.html = re.sub(r'_PRE_', quote.group(), self.html, 1)
            # -------------------------


    def create_headers_id(self):
        unique_slugify = UniqueSlugify()

        def callback(g):
            text = g.group(2)
            id = unique_slugify(text, to_lower=True)
            return '<h{header} id="{id}">{text}</h'.format(header=g.group(1), id=id, text=text)

        regex = re.compile(r"<h(\d)>(.*?)</h", re.MULTILINE)
        self.html = regex.sub(callback, self.html)

    def create_mini_context(self):
        self.mini_context = {
            'title': self.params['title'],
            'short_title': self.params['short_title'],
            'long_title': self.params['long_title'],
            'shortest_title': self.params['short_title'] if self.params['short_title'] else self.params['title'],
            'longest_title': self.params['long_title'] if self.params['long_title'] else self.params['title'],
            'permalink': self.permalink,
            'url': self.url,
            'position': self.params['position'],
            'description': self.params['description'],
            'tags': self.tags
        }

    def create_context(self, site):
        self.context = self.params
        self.context['site'] = site.create_context()
        self.context['shortest_title'] = self.params['short_title'] if self.params['short_title'] else self.params['title']
        self.context['longest_title'] = self.params['long_title'] if self.params['long_title'] else self.params['title']
        self.context['unique_id'] = self.unique_id
        self.context['slug'] = self.slug
        self.context['permalink'] = self.permalink
        self.context['url'] = self.url
        self.context['is_section_index'] = self.is_section_index
        self.context['section_page'] = self.section_page.mini_context if self.section_page else None
        self.context['section_pages'] = [p.mini_context for p in self.section_pages]
        self.context['section_sections'] = sorted([p.mini_context for p in self.section_sections], key=itemgetter('position'))
        self.context['sub_sections'] = sorted([p.mini_context for p in self.sub_sections], key=itemgetter('position'))
        self.context['breadcrumb'] = [p.mini_context for p in self.breadcrumb]
        self.context['tags'] = self.tags
        self.context['toc'] = self.toc

        if self.site.params['enable_shortcodes']:
            self.process_shortcodes()
        if self.site.params['enable_headers_id']:
            self.create_headers_id()
        self.context['content'] = self.html

    def render(self, site: 'Site'):
        """
        1) Récupère le template
        2) Crée le contexte
        3) Rend le template avec le contexte
        """
        try:
            template = site.template_env.get_template(self.params['template'])
        except jinja2.exceptions.TemplateNotFound:
            logging.warning("Unable to find template {template} for {page}".format(template=self.params['template'], page=self.url))

        self.create_context(site=site)

        try:
            self.full_content = template.render(**self.context)
        except Exception as e:
            logging.warning("Unable to render {page}: {exception}".format(page=self.path, exception=e))


class Site(object):
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

        self.default_routes = {
            'tags.html': "/tags",
            'tag.html': "/tags/*",
            'contact.html': "/contact",
            'feed.html': "/rss",
        }

        self.params = {
            'base_url': "",
            'build_dir_name': "public",
            'templates_dir_name': "templates",
            'content_dir_name': "content",
            'static_dir_name': "static",
            'actions_dir_name': "actions",
            'port': 5000,
            'image': "default.jpg",
            'routes': self.default_routes,
            'hooks': {},
            'debug': False,
            'enable_shortcodes': True,
            'enable_headers_id': True,
        }

        self.files = []
        self.pages = {}
        self.pages_list = []
        self.tags = {}

        self.context = {}
        self.build_date = datetime.utcnow()
        self.render_id = None
        self.engine = __version__

        self.script_working_dir = os.path.dirname(os.path.realpath(__file__))

    def load_config(self):
        try:
            f = open(os.path.join(self.base_dir, "config.yaml"), 'r')
            config = f.read()
            f.close()
        except FileNotFoundError:
            logging.error("Unable to load config.yaml file.")
            sys.exit()

        config_params = load_yaml(config, Loader=YamlLoader)
        self.params = {**self.params, **config_params}

        for template, route in self.default_routes.items():
            if template not in self.params['routes']:
                self.params['routes'][template] = route

        if 'tag.html' in self.params['routes'] and not 'tags.html' in self.params['routes']:
            self.params['routes']['tags.html'] = self.params['routes']['tag.html'] + "/"

        self.content_dir = os.path.join(self.base_dir, self.params['content_dir_name'])
        self.static_dir = os.path.join(self.base_dir, self.params['static_dir_name'])
        self.build_dir = os.path.join(self.base_dir, self.params['build_dir_name'])
        self.templates_dir = os.path.join(self.base_dir, self.params['templates_dir_name'])
        self.actions_dir = os.path.join(self.base_dir, self.params['actions_dir_name'])

        self.default_templates_dir = os.path.join(self.script_working_dir, "templates")
        self.template_env = jinja2.Environment(loader=jinja2.FileSystemLoader([self.templates_dir, self.default_templates_dir]), line_statement_prefix='#')

    def load_shortcodes(self):
        global default_shortcodes
        global user_shortcodes

        from victorpy import shortcodes as default_shortcodes

        try:
            load_module(path=os.path.join(self.base_dir, "shortcodes.py"), module_name="user_shortcodes")
            import user_shortcodes
        except:
            pass

    def check_hooks(self):
        for hook_type, actions in self.params['hooks'].items():
            for action in actions:

                action_params = []
                action_parts = action.split("(")
                if len(action_parts) > 1:
                    action = action_parts[0]
                    action_params = action_parts[1].replace(")", "").split(",")

                try:
                    load_module(path=os.path.join(self.actions_dir, action+".py"), module_name=action)
                except Exception:
                    try:
                        load_module(path=os.path.join(self.script_working_dir, self.params['actions_dir_name'], action+".py"), module_name=action)
                    except Exception as e:
                        logging.error("Unable to load hook {action}: {e}".format(action=action, e=e))

    def run_hooks_after_render(self):
        if 'after_render' in self.params['hooks']:
            for action in self.params['hooks']['after_render']:

                action_params = []
                action_parts = action.split("(")
                if len(action_parts) > 1:
                    action = action_parts[0]
                    action_params = action_parts[1].replace(")", "").split(",")

                try:
                    func = getattr(sys.modules[action], "main")
                    func(self, logging, *action_params)
                except Exception as e:
                    logging.error("Unable to execute hook {action}: {e}".format(action=action, e=e))
                finally:
                    os.chdir(self.base_dir)

    def run_hooks_after_build(self):
        if 'after_build' in self.params['hooks']:
            for action in self.params['hooks']['after_build']:

                action_params = []
                action_parts = action.split("(")
                if len(action_parts) > 1:
                    action = action_parts[0]
                    action_params = action_parts[1].replace(")", "").split(",")

                try:
                    func = getattr(sys.modules[action], "main")
                    func(self, logging, *action_params)
                except Exception as e:
                    logging.error("Unable to execute hook {action}: {e}".format(action=action, e=e))
                finally:
                    os.chdir(self.base_dir)

    def load_files(self):
        base_content_path = os.path.join(self.base_dir, "content")

        for root, dirs, files in os.walk(base_content_path):
            for file in files:
                relative_path = os.path.join(root, file).replace(self.content_dir, '')

                try:
                    extension = os.path.splitext(file)[1]
                    if extension == ".md":
                        absolute_path = os.path.join(root, file)
                        f = open(absolute_path, 'r')
                        content = f.read()
                        f.close()
                        self.files.append({'path': relative_path, 'absolute_path': absolute_path, 'content': content})
                except Exception as e:
                    logging.warning("Unable to load file {file}: {e}".format(file=file, e=e))

    def step_1(self):
        """
        - Création des pages de contenu
        - Création du mini_context de chaque page
        - Création des tags
        - Création des pages de tags
        """
        for file in self.files:
            new_page = Page(path=file['path'], site=self, raw_content=file['content'])
            new_page.process_file_content()
            new_page.create_mini_context()

            if 'draft' in new_page.params and new_page.params['draft'] == True:
                continue

            for tag in new_page.params['tags']:
                if not tag in self.tags:
                    self.tags[tag] = {'pages': [new_page], 'title': None, 'permalink': None, 'url': None}
                else:
                    self.tags[tag]['pages'].append(new_page)

                tag_page = [p for p in self.pages_list if p.page_type==PageType.TAG and p.params['title']==tag]
                if not tag_page:
                    tag_page = Page(path=self.params['routes']['tag.html'].replace('*', tag), site=self, raw_content=None, template="tag.html", page_type=PageType.TAG)
                    tag_page.params['title'] = tag
                    self.pages[tag_page.url] = tag_page

                self.tags[tag]['title'] = tag
                self.tags[tag]['permalink'] = tag_page.permalink
                self.tags[tag]['url'] = tag_page.url

                new_page.tags.append({'title': tag, 'url': tag_page.url})

            self.pages[new_page.url] = new_page

        self.pages_list = self.pages.values()

    def step_2(self):
        """
        - Ajout des section_pages à chaque page
        - Ajout des section_sections à chaque page
        - Ajout des sub_sections à chaque page
        - Ajout du fil d'ariane à chaque page
        - Rendu final de la page
        """
        index_pages = [p for p in self.pages_list if p.slug == "index"]

        for page in self.pages_list:
            if page.section_url and page.section_url in self.pages:
                page.section_page = self.pages[page.section_url]
            else:
                page.section_page = None

            page.section_pages = [p for p in self.pages_list if p.section_url == page.section_url and p.slug != "index"]

            if page.parent_section_url:
                page.section_sections = [p for p in index_pages if p.url != "/" and p.section_url == os.path.join(page.parent_section_url, p.direct_section_slug) + "/" and p.url != page.url]

            page.sub_sections = [p for p in index_pages if p.direct_section_slug and page.section_url and p.section_url == os.path.join(page.section_url, p.direct_section_slug) + "/" and p.url != page.url]

            if not page.breadcrumb:
                try:
                    page.breadcrumb = [self.pages["/"]]
                except:
                    page.breadcrumb = []

                if page.url != "/":
                    if page.section_url:
                        breadcrumb_parts = page.section_url.split("/")[1:]
                        for bp in breadcrumb_parts:
                            bp_page = [p for p in index_pages if p.direct_section_slug == bp and p.url != "/"]
                            if bp_page:
                                page.breadcrumb.append(bp_page[0])
                        if page.slug != "index":
                            page.breadcrumb.append(page)
                    else:
                        # TODO: On fait quoi ?
                        pass

            page.render(site=self)

    def create_and_render_auto_pages(self):
        # Page automatiques (sans fichier .md)
        for template, route in self.params['routes'].items():
            new_page = Page(path=route, site=self, raw_content=None, template=template, page_type=PageType.OTHER)
            new_page.render(site=self)
            self.pages[new_page.url] = new_page

    def _create_build_dir(self):
        try:
            shutil.rmtree(self.build_dir)
        except:
            pass
        finally:
            os.makedirs(self.build_dir)

    def _copy_static(self):
        src = os.path.join(self.base_dir, self.params['static_dir_name'])
        dest = os.path.join(self.build_dir, self.params['static_dir_name'])
        try:
            shutil.copytree(src, dest)
        except Exception as e:
            logging.warning("Unable to copy static directory: {src}".format(src=src, exception=e))

    def create_context(self):
        if not self.context:
            self.context = self.params
            self.context['build_date'] = self.build_date
            self.context['render_id'] = self.render_id
            self.context['engine'] = self.engine
            self.context['root_sections'] = sorted([p.mini_context for p in self.pages_list if p.url != "/" and p.slug == "index" and p.parent_section_url == None], key=itemgetter('position'))
            self.context['pages'] = [p.mini_context for p in self.pages_list if p.page_type == PageType.CONTENT]
            self.context['tags'] = OrderedDict({tag: {'title': tag_data['title'], 'permalink': tag_data['permalink'], 'url': tag_data['url'], 'pages': [{'title': p.params['title'], 'permalink': p.permalink, 'url': p.url} for p in tag_data['pages']]} for tag, tag_data in self.tags.items()})
        return self.context

    def _write_files(self):
        for page in self.pages_list:
            os.makedirs(os.path.dirname(page.dest_path), exist_ok=True)
            with open(page.dest_path, 'w') as f:
                f.write(page.full_content)

    def _set_render_id(self):
        self.render_id = hashlib.md5(str(self.build_date).encode('utf-8')).hexdigest()

    def render(self):
        self._set_render_id()
        self.pages = {}
        self.pages_list = []
        self.load_config()
        self.load_shortcodes()
        self.check_hooks()
        self.load_files()
        self.step_1()
        self.step_2()
        self.create_and_render_auto_pages()
        self.run_hooks_after_render()

    def build(self):
        logging.info("Building site...")
        self.render()
        self._create_build_dir()
        self._copy_static()
        self._write_files()
        self.run_hooks_after_build()

    @classmethod
    def build(cls, base_dir):
        site = Site(base_dir=base_dir)
        site.build()

    @classmethod
    def serve(cls, base_dir, port: int):
        site = Site(base_dir=base_dir)
        site.params['port'] = port
        site.render()

        app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"))
        app.debug = True

        @app.route('/internal/open-source/<unique_id>')
        def open_source(unique_id):
            page = [p for p in site.pages.values() if p.unique_id == unique_id][0]
            command = 'open -a "Sublime Text" {file_path}'.format(file_path=page.absolute_path)
            logging.info(command)
            call(command, shell=True)
            return ""

        @app.route('/', defaults={'path': ""})
        @app.route('/<path:path>')
        def dev_server(path):
            try:
                if not path[-1] == "/":
                    path += "/"
            except:
                pass

            try:
                page = site.pages["/" + path]
                full_content = page.full_content

                if site.params['debug'] == True:
                    # TODO: do it anywhere else
                    def json_parser(thing):
                        if type(thing) in (date, datetime):
                            return thing.isoformat()
                        return {}
                    live = """
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.0/gh-fork-ribbon.min.css" />
                        <!--[if lt IE 9]>
                          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.0/gh-fork-ribbon.ie.min.css" />
                        <![endif]-->
                        <a id="open-source" class="github-fork-ribbon" href="#" title="Edit">Edit</a>
                        <script type="text/javascript">
                            if(typeof jQuery == 'undefined'){{document.write('<script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.1.min.js"></'+'script>');}}
                            console.log({page});
                            $('#open-source').on('click', function(){{
                                $.get("/internal/open-source/{unique_id}");
                                return false;
                            }});
                        </script>
                    """.format(page=json.dumps(page.context, default=json_parser), unique_id=page.unique_id)
                    full_content = full_content.replace("</body>", live+"</body>")
                    # ---------------------------

                return full_content
            except Exception as e:
                logging.error(e)
                abort(404)

        # Live reload
        # http://stackoverflow.com/a/9511655
        extra_dirs = [site.content_dir,]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
        app.run(extra_files=extra_files, port=site.params['port'])



def main():
    logging.info("VictorPy " + __version__)

    if not 'serve' in sys.argv and not 'build' in sys.argv:
        sys.argv.append('serve')

    parser = argparse.ArgumentParser(description="A simple yet powerful static site generator")
    parser.add_argument('action', action='store', type=str, choices=('serve', 'build'), help="The action to execute.")
    parser.add_argument('-p', '--port', type=int, default=5000, help="The port number of live server")
    args = parser.parse_args()

    if args.action == 'build':
        Site.build(base_dir=os.getcwd())
    elif args.action == 'serve':
        Site.serve(base_dir=os.getcwd(), port=args.port)

if __name__ == "__main__":
    main()
