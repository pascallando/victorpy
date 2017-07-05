import unittest
import datetime
import time

from pyssm import Site

class TestPyssmMinimal(unittest.TestCase):

    def setUp(self):
        self.site = Site('../data/demo_site_minimal')

    def test_render(self):
        self.site.load_config()
        self.site.load_files()
        self.site.render()

        # self.assertEqual(len(self.site.pages), 1)


class TestPyssm(unittest.TestCase):

    def setUp(self):
        self.site = Site('../data/demo_site')
        self.expected = {
            '/': {
                'url'                : "/",
                'permalink'          : "http://www.victorpy-demosite.com/",
                'slug'               : "index",
                'section_url'        : None,
                'direct_section_slug': None,
                'parent_section_url' : None,
                'sub_sections'       : [],
                'section_pages'      : ['/root-page/'],
                'section_sections'   : [],
            },

            '/root-page/': {
                'url'                : "/root-page/",
                'permalink'          : "http://www.victorpy-demosite.com/root-page/",
                'slug'               : "root-page",
                'section_url'        : None,
                'direct_section_slug': None,
                'parent_section_url' : None,
                'sub_sections'       : [],
                'section_pages'      : ['/root-page/'],
                'section_sections'   : [],
            },

            '/animals/': {
                'url'                : "/animals/",
                'permalink'          : "http://www.victorpy-demosite.com/animals/",
                'slug'               : "index",
                'section_url'        : "/animals/",
                'direct_section_slug': "animals",
                'parent_section_url' : None,
                'sub_sections'       : [],
                'section_pages'      : ['/animals/cat/', '/animals/dog/'],
                'section_sections'   : [],
            },
            '/animals/cat/': {
                'url'                : "/animals/cat/",
                'permalink'          : "http://www.victorpy-demosite.com/animals/cat/",
                'slug'               : "cat",
                'section_url'        : "/animals/",
                'direct_section_slug': "animals",
                'parent_section_url' : None,
                'sub_sections'       : [],
                'section_pages'      : ['/animals/cat/', '/animals/dog/'],
                'section_sections'   : [],
            },
            '/animals/dog/': {
                'url'                : "/animals/dog/",
                'permalink'          : "http://www.victorpy-demosite.com/animals/dog/",
                'slug'               : "dog",
                'section_url'        : "/animals/",
                'direct_section_slug': "animals",
                'parent_section_url' : None,
                'sub_sections'       : [],
                'section_pages'      : ['/animals/cat/', '/animals/dog/'],
                'section_sections'   : [],
            },

            '/food/': {
                'url'                : "/food/",
                'permalink'          : "http://www.victorpy-demosite.com/food/",
                'slug'               : "index",
                'section_url'        : "/food/",
                'direct_section_slug': "food",
                'parent_section_url' : None,
                'sub_sections'       : ["/food/fruits/", "/food/vegetables/"],
                'section_pages'      : ['/food/page-in-food/'],
                'section_sections'   : [],
            },
            '/food/page-in-food/': {
                'url'                : "/food/page-in-food/",
                'permalink'          : "http://www.victorpy-demosite.com/food/page-in-food/",
                'slug'               : "page-in-food",
                'section_url'        : "/food/",
                'direct_section_slug': "food",
                'parent_section_url' : None,
                'sub_sections'       : ["/food/fruits/", "/food/vegetables/"],
                'section_pages'      : ['/food/page-in-food/'],
                'section_sections'   : [],
            },
            '/food/fruits/': {
                'url'                : "/food/fruits/",
                'permalink'          : "http://www.victorpy-demosite.com/food/fruits/",
                'slug'               : "index",
                'section_url'        : "/food/fruits/",
                'direct_section_slug': "fruits",
                'parent_section_url' : "/food/",
                'sub_sections'       : [],
                'section_pages'      : ['/food/fruits/apple/'],
                'section_sections'   : ['/food/vegetables/'],
            },
            '/food/fruits/apple/': {
                'url'                : "/food/fruits/apple/",
                'permalink'          : "http://www.victorpy-demosite.com/food/fruits/apple/",
                'slug'               : "apple",
                'section_url'        : "/food/fruits/",
                'direct_section_slug': "fruits",
                'parent_section_url' : "/food/",
                'sub_sections'       : [],
                'section_pages'      : ['/food/fruits/apple/'],
                'section_sections'   : ['/food/fruits/', '/food/vegetables/'],
            },
            '/food/vegetables/': {
                'url'                : "/food/vegetables/",
                'permalink'          : "http://www.victorpy-demosite.com/food/vegetables/",
                'slug'               : "index",
                'section_url'        : "/food/vegetables/",
                'direct_section_slug': "vegetables",
                'parent_section_url' : "/food/",
                'sub_sections'       : [],
                'section_pages'      : [],
                'section_sections'   : ['/food/fruits/'],
            },
        }

        # print([p['url'] for i, p in self.expected.items() if p['slug'] == "index" and p['parent_section_url'] == None])



    def test_load_config(self):
        self.site.load_config()
        self.assertEqual(self.site.params['base_url'], "http://www.victorpy-demosite.com/")
        self.assertEqual(self.site.params['title'], "Test site")

    def test_load_files(self):
        self.site.load_config()
        self.site.load_files()
        files = [f['path'] for f in self.site.files]
        self.assertListEqual(files, ['/index.md', '/root-page.md', '/animals/cat.md', '/animals/dog.md', '/animals/index.md', '/food/index.md', '/food/page-in-food.md', '/food/fruits/apple.md', '/food/fruits/index.md', '/food/vegetables/index.md'])

    def test_step_1(self):
        s = self.site
        s.load_config()
        s.load_files()
        s.step_1()

        self.assertListEqual(list(s.pages.keys()), ['/', '/tags/cool/', '/root-page/', '/tags/love/', '/animals/cat/', '/animals/dog/', '/animals/', '/food/', '/food/page-in-food/', '/food/fruits/apple/', '/food/fruits/', '/food/vegetables/'])

        for slug, data in self.expected.items():
            self.assertEqual(data['permalink'], s.pages[slug].permalink)

    def test_step_2(self):
        s = self.site
        s.load_config()
        s.load_files()
        s.step_1()
        s.step_2()

        for slug, data in self.expected.items():
            self.assertEqual(data['url'], s.pages[slug].url)
            self.assertEqual(data['slug'], s.pages[slug].slug)
            self.assertEqual(data['section_url'], s.pages[slug].section_url)
            self.assertEqual(data['parent_section_url'], s.pages[slug].parent_section_url)
            self.assertEqual(data['direct_section_slug'], s.pages[slug].direct_section_slug)
            self.assertEqual(data['sub_sections'], [context['url'] for context in s.pages[slug].context['sub_sections']])
            self.assertEqual(data['section_pages'], [context['url'] for context in s.pages[slug].context['section_pages']])
            self.assertEqual(data['section_sections'], [context['url'] for context in s.pages[slug].context['section_sections']])

        root_sections_urls = [s['url'] for s in s.context['root_sections']]
        self.assertListEqual(root_sections_urls, ['/animals/', '/food/'])


    def test_render_pages_dog(self):
        self.site.render()

        page = next(p for p in self.site.pages if p.path == "/animals/dog.md")
        page_context = page.get_context()
        self.assertEqual(page.path, "/animals/dog.md")
        self.assertEqual(page.relative_path, "animals/dog.md")
        self.assertEqual(page.slug, "dog")
        self.assertEqual(page.url, "/animals/dog")
        self.assertEqual(page.permalink, "http://www.victorpy-demosite.com/animals/dog")
        self.assertEqual(page.section_url, "/animals")
        self.assertEqual(page.parent_section_url, "/")
        self.assertEqual(page.direct_section_slug, "animals")
        self.assertEqual(page.dest_path, "../data/demo_site/public/animals/dog/index.html")
        self.assertEqual(page_context['template'], "page.html")
        self.assertEqual(page_context['title'], "The dog")
        self.assertEqual(page_context['long_title'], "This is the dog page")
        self.assertEqual(page_context['description'], None)
        self.assertEqual(page_context['image'], "dog.jpg")
        self.assertEqual(page_context['date'], datetime.date(2016, 10, 15))
        self.assertEqual(page_context['keywords'], ["cool", "love"])
        self.assertEqual(page_context['tags'], ["cool", "love"])
        self.assertEqual(page_context['section_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals", 'description': "The animals page decription", 'position': 0},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food", 'description': None, 'position': 10},
        ])
        self.assertEqual(page_context['section_pages'], [
            {'permalink': "http://www.victorpy-demosite.com/animals/cat", 'url': "/animals/cat", 'title': "The cat", 'description': None, 'position': 0},
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals", 'description': "The animals page decription", 'position': 0},
        ])
        self.assertEqual(page_context['site']['root_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals", 'description': "The animals page decription", 'position': 0},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food", 'description': None, 'position': 10}
        ])
        self.assertEqual(page_context['breadcrumb'], [
            {'permalink': "http://www.victorpy-demosite.com/", 'url': "/", 'title': "Home page", 'description': "Home page description", 'position': 0},
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals", 'description': "The animals page decription", 'position': 0},
            {'permalink': "http://www.victorpy-demosite.com/animals/dog", 'url': "/animals/dog", 'title': "The dog", 'description':None, 'position': 0},
        ])
        self.assertListEqual(list(page_context['site']['tags'].keys()), ['cool', 'love'])
        self.assertListEqual(page_context['tags'], ['cool', 'love'])


    def test_render_pages_apple(self):
        self.site.render()

        page = next(p for p in self.site.pages if p.path == "/food/fruits/apple.md")
        page_context = page.get_context()
        self.assertEqual(page.path, "/food/fruits/apple.md")
        self.assertEqual(page.relative_path, "food/fruits/apple.md")
        self.assertEqual(page.slug, "apple")
        self.assertEqual(page.url, "/food/fruits/apple")
        self.assertEqual(page.permalink, "http://www.victorpy-demosite.com/food/fruits/apple")
        self.assertEqual(page.section_url, "/food/fruits")
        self.assertEqual(page.parent_section_url, "/food")
        self.assertEqual(page.direct_section_slug, "fruits")
        self.assertEqual(page.dest_path, "../data/demo_site/public/food/fruits/apple/index.html")
        self.assertEqual(page_context['template'], "page.html")
        self.assertEqual(page_context['title'], "The apple")
        self.assertEqual(page_context['section_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/food/fruits", 'url': "/food/fruits", 'title': "Fruits"},
            {'permalink': "http://www.victorpy-demosite.com/food/vegetables", 'url': "/food/vegetables", 'title': "Vegetables"},
        ])
        self.assertEqual(page_context['section_pages'], [
            {'permalink': "http://www.victorpy-demosite.com/food/fruits/apple", 'url': "/food/fruits/apple", 'title': "The apple"},
            {'permalink': "http://www.victorpy-demosite.com/food/fruits", 'url': "/food/fruits", 'title': "Fruits"},
        ])
        self.assertEqual(page_context['site']['root_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals"},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food"}
        ])
        self.assertEqual(page_context['breadcrumb'], [
            {'permalink': "http://www.victorpy-demosite.com/", 'url': "/", 'title': "Home page"},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food"},
            {'permalink': "http://www.victorpy-demosite.com/food/fruits", 'url': "/food/fruits", 'title': "Fruits"},
            {'permalink': "http://www.victorpy-demosite.com/food/fruits/apple", 'url': "/food/fruits/apple", 'title': "The apple"},
        ])
        self.assertListEqual(page_context['tags'], [])

    def test_render_pages_food(self):
        self.site.render()

        page = next(p for p in self.site.pages if p.path == "/food/index.md")
        page_context = page.get_context()

        self.assertEqual(page_context['section_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/animals", 'url': "/animals", 'title': "Animals"},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food"},
        ])

        self.assertEqual(page_context['sub_sections'], [
            {'permalink': "http://www.victorpy-demosite.com/food/fruits", 'url': "/food/fruits", 'title': "Fruits"},
            {'permalink': "http://www.victorpy-demosite.com/food/vegetables", 'url': "/food/vegetables", 'title': "Vegetables"}
        ])

        self.assertEqual(page_context['breadcrumb'], [
            {'permalink': "http://www.victorpy-demosite.com/", 'url': "/", 'title': "Home page"},
            {'permalink': "http://www.victorpy-demosite.com/food", 'url': "/food", 'title': "Food"},
        ])
        self.assertListEqual(page_context['tags'], [])

    def test_render_pages_index(self):
        self.site.render()

        page = next(p for p in self.site.pages if p.path == "/index.md")
        page_context = page.get_context()

        self.assertEqual(page_context['breadcrumb'], [
            {'permalink': "http://www.victorpy-demosite.com/", 'url': "/", 'title': "Home page"},
        ])
        self.assertListEqual(page_context['tags'], [])

    def test_render_pages_root_page(self):
        self.site.render()

        page = next(p for p in self.site.pages if p.path == "/root-page.md")
        page_context = page.get_context()

        self.assertEqual(page.path, "/root-page.md")
        self.assertEqual(page.relative_path, "root-page.md")
        self.assertEqual(page.slug, "root-page")
        self.assertEqual(page.url, "/root-page")
        self.assertEqual(page.permalink, "http://www.victorpy-demosite.com/root-page")
        self.assertEqual(page.section_url, "/")
        self.assertEqual(page.parent_section_url, None)
        self.assertEqual(page.direct_section_slug, "")
        self.assertEqual(page.dest_path, "../data/demo_site/public/root-page/index.html")

        self.assertEqual(page_context['breadcrumb'], [
            {'permalink': "http://www.victorpy-demosite.com/", 'url': "/", 'title': "Home page"},
            {'permalink': "http://www.victorpy-demosite.com/root-page", 'url': "/root-page", 'title': "Root page"},
        ])

        self.assertListEqual(page_context['tags'], ['cool'])


class TestPerf(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))

    def test_many_pages(self):
        self.site = Site(base_dir='../data/demo_site_many_pages')
        self.site.render()


if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestSuite()
    # suite.addTest(TestPerf('test_many_pages'))
    suite.addTest(TestPyssm('test_step_2'))
    unittest.TextTestRunner(verbosity=0).run(suite)
