"""just_table.

Table embedding plugin for Pelican
=================================

This plugin allows you to create easily table.

"""
import itertools
import re

from jinja2 import Template
from pelican import signals
from pelican.generators import ArticlesGenerator
from pelican.generators import PagesGenerator

JTABLE_SEPARATOR = "JTABLE_SEPARATOR"
JTABLE_TEMPLATE = "JTABLE_TEMPLATE"
DEFAULT_SEPARATOR = ","

AUTO_INCREMENT_REGEX = re.compile(r"ai ?\= ?\" ?(1) ?\"")
CAPTION_REGEX = re.compile('caption ?= ?"(.+?)"')
SEPARATOR_REGEX = re.compile('separator ?= ?"(.+?)"')
TABLE_HEADER_REGEX = re.compile(r"th ?\= ?\" ?(0) ?\"")
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


def just_table(generator, kira_object):
    """Generate table."""
    if JTABLE_SEPARATOR in generator.settings:
        separator = generator.settings[JTABLE_SEPARATOR]
    else:
        separator = DEFAULT_SEPARATOR

    if JTABLE_TEMPLATE in generator.settings:
        table_template = generator.settings[JTABLE_TEMPLATE]
    else:
        table_template = DEFAULT_TEMPATE

    template = Template(table_template)

    for match in MAIN_REGEX.findall(kira_object._content):
        all_match_str, props, table_data = match
        param = {"ai": 0, "th": 1, "caption": "", "sep": separator}

        if AUTO_INCREMENT_REGEX.search(props):
            param["ai"] = 1
        if CAPTION_REGEX.search(props):
            param["caption"] = CAPTION_REGEX.findall(props)[0]
        if TABLE_HEADER_REGEX.search(props):
            param["th"] = 0
        if SEPARATOR_REGEX.search(props):
            param["sep"] = SEPARATOR_REGEX.findall(props)[0]

        table_data_list = table_data.strip().split("\n")

        if len(table_data_list) >= 1:
            heads = table_data_list[0].split(
                param["sep"]) if param["th"] else None
            if heads:
                bodies = [
                    n.split(param["sep"], len(heads) - 1)
                    for n in table_data_list[1:]
                ]
            else:
                bodies = [n.split(param["sep"]) for n in table_data_list]

            context = generator.context.copy()
            context.update({"heads": heads, "bodies": bodies})
            context.update(param)

            replacement = template.render(context)
            kira_object._content = kira_object._content.replace(
                "".join(all_match_str), replacement
            )


def run_plugin(generators):
    """Run generators on both pages and articles."""
    for generator in generators:
        # [INFO] Set plugin for articles and pages:
        # https://github.com/oumpy/hp_management/blob/928b67170a40259599d636cda2b223b8c4350340/myplugins/skiptags.py
        if isinstance(generator, ArticlesGenerator):
            # [INFO] Articles types:
            # https://github.com/getpelican/pelican/blob/d43b786b300358e8a4cbae4afc4052199a7af762/pelican/generators.py#L288-L296
            for article in itertools.chain(
                    generator.articles, generator.translations,
                    generator.drafts, generator.drafts_translations):
                just_table(generator, article)
        elif isinstance(generator, PagesGenerator):
            # [INFO] Pages types:
            # https://github.com/getpelican/pelican/blob/d43b786b300358e8a4cbae4afc4052199a7af762/pelican/generators.py#L702-L707
            for page in itertools.chain(
                    generator.pages, generator.translations, generator.hidden_pages,
                    generator.hidden_translations, generator.draft_pages, generator.draft_translations):
                just_table(generator, page)


def register():
    """Plugin registration."""
    signals.all_generators_finalized.connect(run_plugin)
