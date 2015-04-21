# -*- coding: utf-8 -*-
"""
Table embedding plugin for Pelican
=================================

This plugin allows you to create easily table.

"""
from __future__ import unicode_literals
import re

regex = re.compile(r"(<p>\[jtable\])(.+)(\[\/jtable\]<\/p>)", re.DOTALL)

table_template = """
<table>
    <thead>
    <tr>
        {% for head in heads %}
        <th align="center">{{ head }}</th>
        {% endfor %}
    </tr>
    </thead>
    <tbody>
        {% for body in bodies %}
        <tr>
            {% for entry in body %}
            <td align="center">{{ entry }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </tbody>
</table>
"""


def generate_table(generator):
    """Replace table tag in the article content."""
    from jinja2 import Template

    template = Template(table_template)

    for article in generator.articles:
        for match in regex.findall(article._content):
            data = match[1].strip().split('\n')
            if len(data) > 2:
                heads = data[0].split(',')
                bodies = [n.split(',') for n in data[1:]]

                # Create a context to render with
                context = generator.context.copy()
                context.update({
                    'heads': heads,
                    'bodies': bodies,
                })

                # Render the template
                replacement = template.render(context)

                article._content = article._content.replace(''.join(match), replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.article_generator_finalized.connect(generate_table)
