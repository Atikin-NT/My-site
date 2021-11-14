from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.footnotes',
        'pymdownx.betterem',
        'pymdownx.emoji',
        'markdown.extensions.footnotes',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.tables',
        'markdown.extensions.abbr',
        'markdown.extensions.md_in_html',
        'pymdownx.caret',
        'pymdownx.details',  # ! добавить css https://facelessuser.github.io/pymdown-extensions/extensions/details/
        'pymdownx.highlight',  # подсветка синтаксиса, проблема css
        'pymdownx.inlinehilite',  # подсветка синтаксиса, проблема css
        'pymdownx.keys',  # подсветка клавиш
        'pymdownx.magiclink',  # ссылки
        'pymdownx.mark',  # выделение текста
        'pymdownx.progressbar',  # прогрессбар
        'pymdownx.smartsymbols',  # спец знаки
        'pymdownx.superfences',  # что-то нужное
        'pymdownx.tabbed',  # вкладки с контентом
        'pymdownx.tasklist',  # выполнил / не выполнил
        'pymdownx.arithmatex',  # матан
        'mdx_math',
])