{%- macro create_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}

{%- macro format_members(namespace) -%}
{%- if namespace["members"]|length -%}

.. csv-table::
    :widths: auto

{% for member_selector in namespace["members"] -%}
    {% set member = api[member_selector] %}
    "{{member["type"]}}", ":ref:`{{ member["name"] }}<{{member_selector}}>`"
{%- endfor %}
{%- endif -%}
{%- endmacro -%}

{% set namespace = api[selector] %}
{{ create_heading(namespace["name"]) }}

{{ format_members(namespace) }}

{% set scope = selector.split('::') -%}
{% for s in scope -%}
{{s}}
{% endfor -%}
