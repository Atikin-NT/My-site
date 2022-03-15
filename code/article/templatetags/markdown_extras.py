from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=[
        'markdown.extensions.footnotes',
        'pymdownx.emoji',  # исправить перенос на новую строку
        'markdown.extensions.footnotes',
        'markdown.extensions.attr_list',
        'markdown.extensions.def_list',
        'markdown.extensions.tables',
        'markdown.extensions.abbr',
        'markdown.extensions.md_in_html',
        'pymdownx.caret',  # ok
        'pymdownx.details',  # ! добавить css https://facelessuser.github.io/pymdown-extensions/extensions/details/
        'pymdownx.highlight',  # подсветка синтаксиса, проблема css
        'pymdownx.superfences',
        'pymdownx.keys',  # подсветка клавиш. На базовом уровне работает
        'pymdownx.mark',  # выделение текста
        'pymdownx.progressbar',  # прогрессбар
        'pymdownx.smartsymbols',  # спец знаки
        'pymdownx.tabbed',  # вкладки с контентом
        'pymdownx.tasklist',  # выполнил / не выполнил, доработать стили!
        'pymdownx.arithmatex',  # матан
        # 'mdx_math',
        # 'markdown_katex',
    ],
                       extension_configs={
        "pymdownx.arithmatex": {
            'generic': True,
        },
       "pymdownx.tasklist": {
           "custom_checkbox": True,
       },
       "pymdownx.highlight": {
           'use_pygments': True,
           'guess_lang': True,
           'noclasses': False,
           'pygments_style': 'friendly',
       },
    })