def prog_name(context):
    return context['site']['prog_name']

def hello(context):
    return "Hello, we're on {page_title}!".format(page_title=context['title'])

def factorial(context, n):
    num = 1
    n = int(n)
    while n >= 1:
        num = num * n
        n = n - 1
    return str(num)