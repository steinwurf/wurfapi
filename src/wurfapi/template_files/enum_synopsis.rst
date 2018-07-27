{% from 'macros.rst' import format_heading %}
{% from 'macros.rst' import format_description %}

{# MERGE_ENUM_DESCRIPTION #}
{%- macro merge_enum_description(enum_value) -%}
{%- if enum_value["briefdescription"] -%}
{{format_description(enum_value["briefdescription"])}}
{%- endif -%}
{%- if enum_value["detaileddescription"] -%}
{{format_description(enum_value["detaileddescription"])}}
{%- endif -%}
{%- endmacro -%}

{% set enum = api[selector] %}
.. _{{selector}}:

{{ format_heading("enum " + enum["name"]) }}

{% if enum["scope"] is not none %}
**Scope:** {{ enum["scope"] }}
{% endif %}

**In header:** ``#include <{{ enum["location"]["file"] }}>``

{% if enum["briefdescription"] %}
Brief Description
-----------------

{{ format_description(enum["briefdescription"]) }}
{% endif %}

{% if enum["values"] %}
Values
------

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Constant
     - Value
     - Description
{% for value in enum["values"] %}
   * - ``{{enum["name"]}}::{{value["name"]}}``
     - {{value["value"]}}
     - {{merge_enum_description(value) | indent(width=7)}}
{% endfor %}
{% endif %}

{% if enum["detaileddescription"] %}
Detailed Description
---------------------

{{ format_description(enum["detaileddescription"]) }}
{% endif %}
