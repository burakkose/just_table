# -*- coding: utf-8 -*-
"""
Table embedding plugin for Pelican
=================================

This plugin allows you to create easily table.

"""
from __future__ import unicode_literals
import re

JTABLE_SEPARATOR = 'JTABLE_SEPARATOR'
JTABLE_TEMPLATE = 'JTABLE_TEMPLATE'
DEFAULT_SEPARATOR = ','

ai_regex = re.compile(r"ai ?\= ?\" ?(1) ?\"")
th_regex = re.compile(r"th ?\= ?\" ?(0) ?\"")
cap_regex = re.compile("caption ?\= ?\"(.+?)\"")
sep_regex = re.compile("separator ?\= ?\"(.+?)\"")
main_regex = re.compile(r"(\[jtable(.*?)\]([\s\S]*?)\[\/jtable\])")

DEFAULT_TEMPATE = """
<div class="justtable">
    <table>
        {% if caption %}
        <caption> {{ caption }} </caption>
        {% endif %}
        {% if th != 0 %}
        <thead>
        <tr>
            {% if ai == 1 %}
            <th> No. </th>
            {% endif %}
            {% for head in heads %}
            <th>{{ head }}</th>
            {% endfor %}
        </tr>
        </thead>
        {% endif %}
        <tbody>
            {% for body in bodies %}
            <tr>
                {% if ai == 1 %}
                <td> {{ loop.index }} </td>
                {% endif %}
                {% for entry in body %}
                <td>{{ entry }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
"""


def generate_table(generator):
    """Replace table tag in the article content."""
    from jinja2 import Template

    # Always good idea to give plugin users to change
    # column separator if they prefer another
    if JTABLE_SEPARATOR in generator.settings:
        separator = generator.settings[JTABLE_SEPARATOR]
    else:
        separator = DEFAULT_SEPARATOR

    # Many people using bootstrap, and prefer to
    # style tables using bootstrap classes.
    # Good idea to give ability to change template
    if JTABLE_TEMPLATE in generator.settings:
        table_template = generator.settings[JTABLE_TEMPLATE]
    else:
        table_template = DEFAULT_TEMPATE

    template = Template(table_template)

    for article in generator.articles + generator.drafts:
        for match in main_regex.findall(article._content):
            param = {"ai": 0, "th": 1, "caption": "", "sep": separator}
            if ai_regex.search(match[1]):
                param['ai'] = 1
            if cap_regex.search(match[1]):
                param['caption'] = cap_regex.findall(match[1])[0]
            if th_regex.search(match[1]):
                param["th"] = 0
            if sep_regex.search(match[1]):
                # Giving ability to use custom column separator to specific tables
                param["sep"] = sep_regex.findall(match[1])[0]
            data = match[2].strip().split('\n')
            if len(data) > 2 or len(data) == 1 and param['th'] == 0:
                if param['th'] != 0:
                    heads = data[0].split(param["sep"])
                    begin = 1
                else:
                    heads = None
                    begin = 0

                if begin == 1:
                    # If we have header, we already know how much columns
                    # we have and no need to split more to columns.
                    bodies = [n.split(param["sep"], len(heads) - 1) for n in data[begin:]]
                else:
                    bodies = [n.split(param["sep"]) for n in data[begin:]]

                # Create a context to render with
                context = generator.context.copy()
                context.update({
                    'heads': heads,
                    'bodies': bodies,
                })
                context.update(param)

                # Render the template
                replacement = template.render(context)
                article._content = article._content.replace(''.join(match[0]), replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.article_generator_finalized.connect(generate_table)
