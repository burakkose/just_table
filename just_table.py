# -*- coding: utf-8 -*-
"""
Table embedding plugin for Pelican
=================================

This plugin allows you to create easily table.

"""
from __future__ import unicode_literals

import re
import logging
logger = logging.getLogger(__name__)

JTABLE_SEPARATOR = 'JTABLE_SEPARATOR'
JTABLE_TEMPLATE = 'JTABLE_TEMPLATE'
DEFAULT_SEPARATOR = ','

AUTO_INCREMENT_REGEX = re.compile(r"^ai\s*=\s*\&rdquo;(.+)\&rdquo")
TABLE_HEADER_REGEX = re.compile(r"^th\s*=\s*\&rdquo;(.+)\&rdquo")
CAPTION_REGEX = re.compile(r"^caption\s*=\s*\&rdquo;(.+)\&rdquo;")
SEPARATOR_REGEX = re.compile(r"^separator\s*=\s*\&rdquo;(.+)\&rdquo;")
MAIN_REGEX = re.compile(r"(\[jtable\s*(.*?)\]([\s\S]*?)\[\/jtable\])")

DEFAULT_TEMPATE = """
<div class="justtable">
    <table class="justtable">
        {%- if caption %}
        <caption> {{ caption }} </caption>
        {%- endif %}
        {%- if th != 0 %}
        <thead class="justtable">
        <tr class="justtable">
            {%- if ai == 1 %}
            <th class="justtable"> No. </th>
            {%- endif %}
            {%- for head in heads %}
            <th class="justtable">{{ head }}</th>
            {%- endfor %}
        </tr>
        </thead>
        {%- endif %}
        <tbody class="justtable">
            {%- for body in bodies %}
            <tr class="justtable">
                {%- if ai == 1 %}
                <td class="justtable"> {{ loop.index }} </td>
                {%- endif %}
                {%- for entry in body %}
                <td class="justtable">{{ entry }}</td>
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
    logger.warning("default separator : '%s'", separator)

    if JTABLE_TEMPLATE in generator.settings:
        table_template = generator.settings[JTABLE_TEMPLATE]
    else:
        table_template = DEFAULT_TEMPATE
    logger.warning("default template: '%s':", table_template)


    template = Template(table_template)

    for article in generator.articles + generator.drafts:
        for match in MAIN_REGEX.findall(article._content):
            all_match_str, props, table_data = match
            param = {"ai": 0, "th": 1, "caption": "", "sep": separator}
            logger.info("Jump table bracket content: '%s'", all_match_str)
            logger.info("props: '%s'", props)

            if SEPARATOR_REGEX.search(props):
                separator = SEPARATOR_REGEX.findall(props)[0]
                logger.info("***********SEPARATOR_REGEX.search(props): '%s'", 
                               str(SEPARATOR_REGEX.findall(props)[0]))
            else:
                logger.info("No 'separator' found")
            if AUTO_INCREMENT_REGEX.search(props):
                param['ai'] = 1
                logger.("ai: '%s'", ai)
            if CAPTION_REGEX.search(props):
                param['caption'] = CAPTION_REGEX.findall(props)[0]
                logger.warning("caption: '%s'", param['caption'])
            if TABLE_HEADER_REGEX.search(props):
                param["th"] = 0
                logger.warning("***********th: %s", th)
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
