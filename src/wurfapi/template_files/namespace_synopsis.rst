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
    "{{member["type"]}}", ":ref:`{{ member["name"] }} <{{member_selector}}>`"
{%- endfor %}
{%- endif -%}
{%- endmacro -%}

{% set namespace = api[selector] %}

.. _{{selector}}:

{{ create_heading("Namespace: " + namespace["name"]) }}

{% if namespace["scope"] %}
**Scope:** {{ namespace["scope"] }}
{% endif %}

{{ format_members(namespace) }}




{% from 'function_synopsis.rst' import format_function %}

{% set functions = api_filter(
       api, namespace["members"], type="function")
%}

{% if functions %}

Namespace Function Description
------------------------------

{% for function in functions -%}
    {{ format_function(api, function) }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}



