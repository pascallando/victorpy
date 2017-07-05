import re

version = None

def prog_name(context):
    global version

    if not version:
        version = re.search(
            '^__version__\s*=\s*["\'](.*)["\']',
            open('../victorpy/__init__.py').read(),
            re.M
        ).group(1)

    return "VictorPy " + version

def hello(context):
    return "Hello, we're on {page_title}!".format(page_title=context['title'])

def factorial(context, n):
    num = 1
    n = int(n)
    while n >= 1:
        num = num * n
        n = n - 1
    return str(num)

