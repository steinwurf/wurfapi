{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_paragraphs -%}
{%- from 'macros.rst' import merge_description -%}

{% set defines = api | api_filter(kind="define") %}

{% if defines %}

Defines
-------

{% for define in defines -%}
{% set define = api[define] %}
{% if "initializer" in define %}
``#define {{ define["name"] }} = {{ define["initializer"] }}``
{% else %}
``#define {{ define["name"] }}``
{% endif %}

{% if define["location"]["include"] %}
**In header:** ``#include <{{ define["location"]["include"] }}>``
{% endif %}

{{ "-----" if not loop.last }}

{% endfor -%}

{% endif %}

