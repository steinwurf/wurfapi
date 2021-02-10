{% import 'macros.rst' as macros with context -%}


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
   :align: left

{% for selector in selectors %}
   * - {{ api[selector]["kind"] }}
     - :ref:`{{ api[selector]["name"] }}<{{selector}}>` {{ format_member_type_values(selector) }}
{% endfor %}

{% endmacro -%}

{# FORMAT_MEMBER_VARIABLES_TABLE #}
{%- macro format_member_variables_table(selectors) -%}

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: left

   * - Type
     - Name
     - Value
     - Description
{% for selector in selectors %}
{%- set variable = api[selector] %}
   * - {{ macros.format_type_list(variable["type"]) }}
     - {{ variable["name"] }}
     - {{ variable["value"] }}
     - {{ macros.merge_description(variable) | indent(width=7) }}
{% endfor %}
{% endmacro -%}

{% set class = api[selector] %}

.. _{{selector}}:

{{ macros.format_heading(class["kind"] + " " + class["name"]) }}

{% if class["scope"] %}
**Scope:** {{ class["scope"] }}
{% endif %}

{% if class["location"]["include"] %}
**In header:** ``#include <{{ class["location"]["include"] }}>``
{% endif %}

{% if class["briefdescription"] %}
Brief description
-----------------
{{ macros.format_paragraphs(class["briefdescription"]) }}
{% endif %}

{% if class["template_parameters"] %}
Template parameters
-------------------

.. code-block:: c++

     template {{ macros.format_template_parameters(class["template_parameters"], as_code=True) }}
     {{ class["kind"] }} {{ class["name"] }}

{% if class["template_parameters"] | selectattr("description") | list | count -%}
More information in the :ref:`template parameter <{{selector}}_template_parameter_description>`
description section.
{% endif %}

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

{{ macros.format_function_table(functions) }}

{% endif %}


{% set functions = class["members"] | api_filter(
       kind="function", access="public", is_static=true)
%}

{%- if functions -%}

Static member functions (public)
--------------------------------

{{ macros.format_function_table(functions) }}

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
{{ macros.format_paragraphs(class["detaileddescription"]) }}
{% endif %}


{% set functions = class["members"]
       | api_filter(kind="function", access="public")
       | api_sort(keys=["location", "line"])
%}

{% if functions %}

Member Function Descriptions
----------------------------

{% for function in functions -%}
    {{ macros.format_function(function) }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}


{% set types = class["members"]
       | api_filter(kind=["typedef", "using"], access="public")
       | api_sort(keys=["location", "line"])
%}

{% if types %}

Type Description
----------------

{% for selector in types -%}

.. _{{selector}}:

{{ macros.format_type_alias(api[selector]) }}

    {{ macros.format_paragraphs(api[selector]["briefdescription"])|indent }}

    {{ macros.format_paragraphs(api[selector]["detaileddescription"])|indent }}

{{ "-----" if not loop.last }}

{% endfor %}


{% endif %}

{# FORMAT_MEMBER_VARIABLES_TABLE #}
{%- macro format_template_parameter_table(template_parameters) -%}

.. list-table::
   :header-rows: 1
   :widths: auto
   :align: left

   * - Type
     - Default
     - Description
{% for parameter in template_parameters -%}
{%- set type = parameter["type"] | default([]) -%}
{%- set name = parameter["name"] | default("")-%}
{%- set default = parameter["default"] | default([]) -%}
{%- set description = parameter["description"] | default([]) %}
   * - {{ macros.format_type_list(type) }} {{ name }}
     - {{ macros.format_type_list(default) }}
     - {{ macros.format_paragraphs(description) | indent(width=7) }}
{% endfor %}
{% endmacro -%}

{% if class["template_parameters"] | selectattr("description") | list | count -%}
Template parameter description
------------------------------

.. _{{selector}}_template_parameter_description:

{{ macros.format_template_parameters_description(class["template_parameters"]) }}

{% endif %}
