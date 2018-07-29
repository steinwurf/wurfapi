
{% from 'macros.rst' import format_heading %}
{% from 'function_synopsis.rst' import format_function %}


{# FORMAT_MEMBER_TABLE #}

{%- macro format_member_table(selectors) -%}
.. list-table::
   :header-rows: 0
   :widths: auto

{% for selector in selectors %}
   {%- set member = api[selector] %}

   * - {{ member["type"] }}
     - :ref:`{{ member["name"] }}<{{selector}}>`
{% endfor %}

{% endmacro -%}

{% set namespace = api[selector] %}

.. _{{selector}}:

{{ format_heading("namespace " + namespace["name"]) }}

{% if namespace["scope"] %}
**Scope:** {{ namespace["scope"] }}
{% endif %}

{% if namespace["members"] %}

{{ format_member_table(namespace["members"]) }}

{% endif %}

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
