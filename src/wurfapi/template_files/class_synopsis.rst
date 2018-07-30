{% from 'macros.rst' import format_heading %}
{% from 'macros.rst' import format_description %}
{% from 'function_synopsis.rst' import format_function %}
{% from 'function_synopsis.rst' import format_parameters %}


{# FORMAT_MEMBER_TABLE #}

{%- macro format_member_table(selectors) -%}
.. list-table::
   :header-rows: 0
   :widths: auto

{% for selector in selectors %}
   {%- set function = api[selector] %}
   {%- set signature = format_parameters(function["parameters"]) %}
   {%- set signature = signature + " const" if function["is_const"]
           else signature %}
   {%- set return_type = function["return_type"] %}
   {%- set return_type = "virtual " + return_type if function["is_virtual"]
           else return_type %}

   * - {{ return_type }}
     - :ref:`{{ function["name"] }}<{{selector}}>` {{ signature }}
{% endfor %}

{% endmacro -%}


{% set class = api[selector] %}

.. _{{selector}}:

{{ format_heading(class["type"] + " " + class["name"]) }}

{% if class["scope"] %}
**Scope:** {{ class["scope"] }}
{% endif %}

**In header:** ``#include <{{ class["location"]["file"] }}>``

{% if class["briefdescription"] %}
Brief description
-----------------
{{ format_description(class["briefdescription"]) }}
{% endif %}


{% set functions = api_filter(
       api, class["members"], type="function", access="public", is_static=false)
%}

{%- if functions -%}
Member functions (public)
-------------------------

{{ format_member_table(functions) }}

{% endif %}


{% set functions = api_filter(
       api, class["members"], type="function", access="public", is_static=true)
%}

{%- if functions -%}
Static member functions (public)
--------------------------------

{{ format_member_table(functions) }}

{%- endif -%}


{% if class["detaileddescription"] %}
Description
-----------
{{ format_description(class["detaileddescription"]) }}
{% endif %}


{% set functions = api_filter(
       api, class["members"], type="function", access="public")
%}

{% if functions %}

Member Function Description
---------------------------

{% for function in functions -%}
    {{ format_function(api, function) }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}


