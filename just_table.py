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

AUTO_INCREMENT_REGEX = re.compile(r"ai ?\= ?\" ?(1) ?\"")
TABLE_HEADER_REGEX = re.compile(r"th ?\= ?\" ?(0) ?\"")
CAPTION_REGEX = re.compile("caption ?\= ?\"(.+?)\"")
SEPARATOR_REGEX = re.compile("separator ?\= ?\"(.+?)\"")
MAIN_REGEX = re.compile(r"(\[jtable(.*?)\]([\s\S]*?)\[\/jtable\])")

DEFAULT_TEMPATE = """
<div class="justtable">
    <table>
        {%- if caption %}
        <caption> {{ caption }} </caption>
        {%- endif %}
        {%- if th != 0 %}
        <thead>
        <tr>
            {%- if ai == 1 %}
            <th> No. </th>
            {%- endif %}
            {%- for head in heads %}
            <th>{{ head }}</th>
            {%- endfor %}
        </tr>
        </thead>
        {%- endif %}
        <tbody>
            {%- for body in bodies %}
            <tr>
                {%- if ai == 1 %}
                <td> {{ loop.index }} </td>
                {%- endif %}
                {%- for entry in body %}
                <td>{{ entry }}</td>
                {%- endfor %}
            </tr>
            {%- endfor %}
        </tbody>
    </table>
</div>
"""


def generate_table(generator):
    from jinja2 import Template

    if JTABLE_SEPARATOR in generator.settings:
        separator = generator.settings[JTABLE_SEPARATOR]
    else:
        separator = DEFAULT_SEPARATOR

    if JTABLE_TEMPLATE in generator.settings:
        table_template = generator.settings[JTABLE_TEMPLATE]
    else:
        table_template = DEFAULT_TEMPATE

    template = Template(table_template)

    for article in generator.articles + generator.drafts:
        for match in MAIN_REGEX.findall(article._content):
            all_match_str, props, table_data = match
            param = {"ai": 0, "th": 1, "caption": "", "sep": separator}

            if AUTO_INCREMENT_REGEX.search(props):
                param['ai'] = 1
            if CAPTION_REGEX.search(props):
                param['caption'] = CAPTION_REGEX.findall(props)[0]
            if TABLE_HEADER_REGEX.search(props):
                param["th"] = 0
            if SEPARATOR_REGEX.search(props):
                param["sep"] = SEPARATOR_REGEX.findall(props)[0]

            table_data_list = table_data.strip().split('\n')

            if len(table_data_list) >= 1:
                heads = table_data_list[0].split(param["sep"]) if param['th'] else None
                if heads:
                    bodies = [n.split(param["sep"], len(heads) - 1) for n in table_data_list[1:]]
                else:
                    bodies = [n.split(param["sep"]) for n in table_data_list]

                context = generator.context.copy()
                context.update({
                    'heads': heads,
                    'bodies': bodies,
                })
                context.update(param)

                replacement = template.render(context)
                article._content = article._content.replace(''.join(all_match_str), replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.article_generator_finalized.connect(generate_table)
