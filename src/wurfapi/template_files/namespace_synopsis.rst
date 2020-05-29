{% import 'macros.rst' as macros with context -%}

{# FORMAT_MEMBER_TABLE #}

{% macro format_member_table(selectors) %}
.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left

{% for selector in selectors %}
   {%- set member = api[selector] %}

   * - {{ member["kind"] }}
     - {{ macros.format_ref(member["name"], selector )}}

{%- endfor -%}

{%- endmacro -%}

{%- set namespace = api[selector] -%}

.. _{{selector}}:

{{ macros.format_heading("namespace " + namespace["name"]) }}

{% if namespace["scope"] %}
**Scope:** {{ namespace["scope"] }}

{% endif -%}

{% if namespace["members"] %}

{{ format_member_table(namespace["members"]) }}

{% endif -%}

{% set functions = namespace["members"] | api_filter(
       kind="function")
-%}

{% if functions %}

Functions
---------

{% for function in functions -%}
    {{ macros.format_function(function) }}

{{ "-----" if not loop.last }}

{% endfor -%}
{% endif %}

