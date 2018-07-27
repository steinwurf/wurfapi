
{% from 'function_synopsis.rst' import format_function %}
{% from 'macros.rst' import format_heading %}

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

{{ format_heading("namespace " + namespace["name"]) }}

{% if namespace["scope"] %}
**Scope:** {{ namespace["scope"] }}
{% endif %}

{{ format_members(namespace) }}

{% set functions = api_filter(
       api, namespace["members"], type="function")
%}

{% if functions %}

Functions
---------

{% for function in functions -%}
    {{ format_function(api, function) }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}
