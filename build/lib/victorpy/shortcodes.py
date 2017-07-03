from jinja2 import Template
import requests

def sectionpages(context):
    template = Template("""
        <div class="list-group">
            {% for page in (section_pages + sub_sections)|sort(attribute='position') %}
                <a class="list-group-item" href="{{ page.url }}">
                    <h4 class="list-group-item-heading">
                        {{ page.title }}
                    </h4>
                    <p class="list-group-item-text text-muted small">
                        {% if page.description %}
                            {{ page.description }}<br />
                        {% endif %}
                        {% for tag in page.tags %}
                            <small class="label label-primary label-tag">{{ tag.title }}</small>
                        {% endfor %}
                    </p>
                </a>
            {% endfor %}
        </div>
    """)
    return template.render(sub_sections=context['sub_sections'], section_pages=context['section_pages'])

def figure(context, src, alt, caption=None):
    if not caption:
        caption = alt
    template = Template("""
        <figure>
            <img src="{{ src }}" alt="{{ caption }}" class="img-responsive">
            <figcaption>
                <p><span style="font-variant-caps: small-caps">Figure – </span>{{ caption }}</p>
            </figcaption>
        </figure>
    """)
    return template.render(src=src, caption=caption)

def amazon(context, code_type, asin, title=None):
    if code_type == 'image':
        template = Template("""<a href="http://www.amazon.fr/gp/product/{{ asin }}/ref=as_li_ss_il?ie=UTF8&camp=1642&creative=19458&creativeASIN={{ asin }}&linkCode=as2&tag={{ amazon_id }}"><img src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={{ asin }}&Format=_SL160_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1" alt="Article" /></a>""")
    elif code_type == 'snippet':
        template = Template("""<div class="thumbnail text-center" style="width:200px"><img src="http://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={{ asin }}&Format=_SL160_&ID=AsinImage&MarketPlace=FR&ServiceVersion=20070822&WS=1" alt="Article" /><div class="caption">{% if title %}<h4>{{ title }}</h4>{% endif %}<p><a href="http://www.amazon.fr/gp/product/{{ asin }}/ref=as_li_ss_il?ie=UTF8&camp=1642&creative=19458&creativeASIN={{ asin }}&linkCode=as2&tag={{ amazon_id }}" class="btn btn-primary"><span class="fa fa-play"></span> Voir</a></p></div></div>""")
    else:
        template = Template("http://www.amazon.fr/gp/product/{{ asin }}/ref=as_li_ss_il?ie=UTF8&camp=1642&creative=19458&creativeASIN={{ asin}}&linkCode=as2&tag={{ amazon_id }}")

    if 'amazon_id' in context['site']:
        amazon_id = context['site']['amazon_id']
    else:
        amazon_id = ""

    return template.render(code_type=code_type, asin=asin, title=title, amazon_id=amazon_id)


def tweet(context, id):
    response = requests.get("https://api.twitter.com/1/statuses/oembed.json?id="+id).json()
    return response['html']

def alert(context, type="success", title=None):
    if title:
        return Template("""<div class="alert alert-{{ type }}"><strong style="font-variant: small-caps">{{ title }}</strong> –""").render(type=type, title=title)
    else:
        return Template("""<div class="alert alert-{{ type }}">""").render(type=type)

def endalert(context):
    return '</div>'

def row(context):
    return '<div class="row">'

def endrow(context):
    return '</div>'

def col(context, width):
    return Template('<div class="col-md-{{ width }} col-lg-{{ width }}">').render(width=width)

def endcol(context):
    return '</div>'

def pull(context, where):
    return Template("""<div class="pull-{{ where }}" style="margin-left: 5px">""").render(where=where)

def endpull(context):
    return '</div>'
