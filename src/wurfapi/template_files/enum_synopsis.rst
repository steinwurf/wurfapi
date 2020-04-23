{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_paragraphs -%}
{%- from 'macros.rst' import merge_description -%}

{% set enum = api[selector] %}
.. _{{selector}}:

{{ format_heading("enum " + enum["name"]) }}

{% if enum["scope"] is not none %}
**Scope:** {{ enum["scope"] }}
{% endif %}

{% if enum["location"]["include"] %}
**In header:** ``#include <{{ enum["location"]["include"] }}>``
{% endif %}

{% if enum["briefdescription"] %}
Brief Description
-----------------

{{ format_paragraphs(enum["briefdescription"]) }}
{% endif %}

{% if enum["values"] %}
Values
------

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: left

   * - Constant
     - Value
     - Description
{% for value in enum["values"] %}
   * - ``{{enum["name"]}}::{{value["name"]}}``
     - {{value["value"]}}
     - {{merge_description(value) | indent(width=7)}}
{% endfor %}
{% endif %}

{% if enum["detaileddescription"] %}
Detailed Description
---------------------

{{ format_paragraphs(enum["detaileddescription"]) }}
{% endif %}
