{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_description -%}
{%- from 'macros.rst' import format_type_to_link -%}
{%- from 'macros.rst' import format_type_alias -%}
{%- from 'macros.rst' import merge_description -%}
{%- from 'macros.rst' import format_function -%}
{%- from 'macros.rst' import format_parameters -%}

{# FORMAT_MEMBER_TABLE_ROW #}

{%- macro format_member_table_row(selector) -%}
{%- set function = api[selector] %}
{%- set signature = format_parameters(function["parameters"]) %}
{%- set signature = signature + " const" if function["is_const"] else signature %}
{%- set return_type = format_type_to_link(function["return"]["type"]) %}
{%- set return_type = "virtual " + return_type if function["is_virtual"] else return_type -%}
* - {{ return_type }}
  - :ref:`{{ function["name"] }}<{{selector}}>` {{ signature }}
{% endmacro -%}

{# FORMAT_MEMBER_TABLE #}

{%- macro format_member_table(selectors) -%}
.. list-table::
   :header-rows: 0
   :widths: auto

{% for selector in selectors | api_sort(key="name", reverse=False)
                             | api_sort(key="is_destructor")
                             | api_sort(key="is_constructor") %}
   {{ format_member_table_row(selector) | indent(width=3) }}
{%- endfor -%}

{% endmacro -%}

{# FORMAT_MEMBER_TYPE_VALUES #}

{%- macro format_member_type_values(selector) -%}
{%- if api[selector]["kind"] == "enum" -%}
{%- set values = [] -%}
{%- for value in api[selector]["values"]  -%}
{%- do values.append(value["name"]) -%}
{%- endfor -%}
{ {{ values | join(", ") }} }
{%- endif -%}
{%- endmacro -%}

{# FORMAT_MEMBER_TYPE_TABLE #}

{%- macro format_member_type_table(selectors) -%}
.. list-table::
   :header-rows: 0
   :widths: auto

{% for selector in selectors %}
   * - {{ api[selector]["kind"] }}
     - :ref:`{{ api[selector]["name"] }}<{{selector}}>` {{ format_member_type_values(selector) }}
{%- endfor -%}

{% endmacro -%}

{# FORMAT_MEMBER_VARIABLES_TABLE #}
{%- macro format_member_variables_table(selectors) -%}

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Type
     - Name
     - Value
     - Description
{% for selector in selectors %}
{%- set variable = api[selector] %}
   * - {{ format_type_to_link(variable["type"]) }}
     - {{ variable["name"] }}
     - {{ variable["value"] }}
     - {{ merge_description(variable) | indent(width=7) }}
{% endfor %}
{% endmacro -%}

{% set class = api[selector] %}

.. _{{selector}}:

{{ format_heading(class["kind"] + " " + class["name"]) }}

{% if class["scope"] %}
**Scope:** {{ class["scope"] }}
{% endif %}

**In header:** ``#include <{{ class["location"]["file"] }}>``

{% if class["briefdescription"] %}
Brief description
-----------------
{{ format_description(class["briefdescription"]) }}
{% endif %}

{% set types = class["members"]
       | api_filter(kind=["class", "struct", "enum", "using", "typedef"], access="public")
%}

{%- if types -%}
Member types (public)
---------------------

{{ format_member_type_table(types) }}

{% endif -%}


{% set functions = class["members"]
       | api_filter(kind="function", access="public", is_static=false)
%}

{%- if functions -%}
Member functions (public)
-------------------------

{{ format_member_table(functions) }}

{% endif %}


{% set functions = class["members"] | api_filter(
       kind="function", access="public", is_static=true)
%}

{%- if functions -%}

Static member functions (public)
--------------------------------

{{ format_member_table(functions) }}

{% endif %}

{% set variables = class["members"]
       | api_filter(kind="variable", access="public", is_static=false)
%}

{%- if variables -%}

Member variables (public)
-------------------------

{{ format_member_variables_table(variables) }}

{% endif %}


{% set variables = class["members"]
       | api_filter(kind="variable", access="public", is_static=true)
%}

{%- if variables -%}

Static member variables (public)
--------------------------------

{{ format_member_variables_table(variables) }}

{% endif %}

{% if class["detaileddescription"] %}
Description
-----------
{{ format_description(class["detaileddescription"]) }}
{% endif %}


{% set functions = class["members"]
       | api_filter(kind="function", access="public")
       | api_sort(key="name", reverse=False)
       | api_sort(key="is_destructor")
       | api_sort(key="is_constructor")
%}

{% if functions %}

Member Function Description
---------------------------

{% for function in functions -%}
    {{ format_function(api, function) }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}


{% set types = class["members"]
       | api_filter(kind=["typedef", "using"], access="public")
       | api_sort(key="name", reverse=False)
%}

{% if types %}

Type Description
----------------

{% for selector in types -%}

.. _{{selector}}:

{{ format_type_alias(api[selector]) }}
    {{ format_description(api[selector]["briefdescription"])|indent }}

    {{ format_description(api[selector]["detaileddescription"])|indent }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}




