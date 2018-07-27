{%- macro create_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}

{%- macro create_class_heading(class, char='=') -%}
{%- set name = class["type"] + " " + class["name"] -%}
{{ create_heading(name, char) }}
{%- endmacro -%}

{%- macro create_function_heading(function) -%}
{%- set name = function["return_type"] + " " + function["signature"] -%}
{%- if function["is_static"] %} {%- set name = name + " ``[static]``" %}{%endif%}
{%- if function["is_virtual"] %} {%- set name = name + " ``[virtual]``" %}{%endif%}
{{ create_heading(name, ".") }}
{%- endmacro -%}

{%- macro create_function_signature(unique_name, function) -%}
{# We build the signature of a function as a list of strings #}
{%- set signature = [":ref:`", function["name"], "<", unique_name, ">`"] -%}
{%- do signature.append(" **(** ") -%}
{%- set parameters = [] -%}
{%- for p in function["parameters"] -%}
    {%- do parameters.append(p["type"] + " " + p["name"]) -%}
{%- endfor -%}
{%- do signature.append(parameters|join(', ')) -%}
{%- do signature.append(" **)** ") -%}
{%- if function["is_const"] -%}
{%- do signature.append("const") -%}
{%- endif -%}
{{ signature|join("") -}}
{%- endmacro -%}

{%- macro format_code_block(paragraph) %}

.. code-block:: c++

{{ paragraph["content"] | indent(first=true) }}

{% endmacro -%}

{%- macro format_code_inline(paragraph) -%}
``{{ paragraph["content"] }}``{{ " " }}
{%- endmacro -%}

{%- macro format_code(paragraph) -%}
{%- if paragraph["is_block"] -%}
    {{ format_code_block(paragraph) }}
{%- else -%}
    {{ format_code_inline(paragraph) }}
{%- endif -%}
{%- endmacro -%}

{# FORMAT_TEXT_LINK #}

{%- macro format_text_link(paragraph) -%}
:ref:`{{ paragraph["content"] }}<{{ paragraph["link"] }}>`
{%- endmacro -%}

{# FORMAT_TEXT #}

{%- macro format_text(paragraph) -%}

{%- if "link" in paragraph -%}
    {{ format_text_link(paragraph) }}
{%- else -%}
    {{ paragraph["content"] }}
{%- endif -%}
{{ " " }}
{%- endmacro -%}

{# PRINT_DESCRIPTION #}
{%- macro print_description(description) -%}
{%- for para in description -%}
    {% if para["type"] == "text" -%}
        {{ format_text(para) }}
    {%- endif -%}
    {%- if para["type"] == "code" -%}
        {{ format_code(para) }}
    {%- endif -%}
{%- endfor -%}
{%- endmacro -%}

{# FORMAT_MEMBER_FUNCTIONS #}
{%- macro format_member_functions(type, static) -%}

{%- set members = [] -%}

{%- for member_selector in type["members"] -%}
    {% set member = api[member_selector] -%}
    {%- if member["type"] in ["function"] -%}
    {%- if member["access"] in ["public"] -%}
    {%- if member["is_static"] == static -%}
        {%- do members.append(member_selector) -%}
    {%- endif -%}
    {%- endif -%}
    {%- endif -%}
{%- endfor %}
{%- if members|length -%}

.. csv-table::
    :widths: auto

{% for member_selector in members -%}
    {% set member = api[member_selector] %}
    "{% if member["is_virtual"] -%}{{"virtual "}}{%- endif -%}{{member["return_type"]}}", "{{- create_function_signature(member_selector, member) }}"
{%- endfor %}
{%- endif -%}
{%- endmacro -%}

{# FORMAT_RETURN_DESCRIPTION #}
{%- macro format_return_description(type, description) -%}
{%- if description|length -%}
{% set description = print_description(description) %}
Returns:
{{ description | indent(first=true) }}
{%- endif -%}
{%- endmacro -%}

{# FORMAT_PARAMETER_DESCRIPTION #}
{%- macro format_parameter_description(parameter) -%}
{%- if parameter["description"]|length -%}
{% set description = print_description(parameter["description"]) %}
``{{parameter["name"]}}``:
{{ description | indent(first=true) }}
{%- endif -%}
{%- endmacro -%}


{% set class = api[selector] %}

.. _{{selector}}:

{{ create_class_heading(class, "=") }}

{% if class["scope"] is not none %}
**Scope:** {{ class["scope"] }}
{% endif %}

**In header:** ``#include <{{ class["location"]["file"] }}>``

{% if class["briefdescription"] %}
Brief description
-----------------
{{ print_description(class["briefdescription"]) }}
{% endif %}

{% set member_description -%}
{{ format_member_functions(api[selector], static=false) }}
{%- endset %}

{% if member_description %}
Member functions (public)
-------------------------

{{ member_description }}

{% endif %}

{% set member_description -%}
{{ format_member_functions(api[selector], static=true) }}
{%- endset %}

{% if member_description | length %}
Static member functions (public)
--------------------------------

{{member_description}}

{% endif %}

{% if class["detaileddescription"] %}
Description
-----------
{{ print_description(class["detaileddescription"]) }}
{% endif %}

{% from 'function_synopsis.rst' import format_function %}

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


