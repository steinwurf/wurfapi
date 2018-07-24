{%- macro create_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}

{%- macro create_class_heading(class, char='=') -%}
{%- set name = class["type"] + " " + class["name"] -%}
{{ create_heading(name, char) }}
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

{%- macro create_function_heading(function) -%}
{# We build the signature of a function as a list of strings #}
{{ function["return_type"] + " " + function["signature"] + " ``[static]``" }}
{%- endmacro -%}

{%- macro print_description(description) -%}
{%- set output = [] -%}
{%- for para in description -%}
    {% if para["type"] == "text" -%}
        {%- if "link" in para -%}
            {%- set link = ":ref:`"+para["content"]+"<" +para["link"] +">`" -%}
            {%- do output.append(link) -%}
        {% else %}
            {%- do output.append(para["content"]) -%}
        {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{{ output|join(" ") -}}
{%- endmacro -%}


{%- macro create_function_description(unique_name, function) -%}
{# First element is a label to the unique_name #}
.. _{{unique_name}}:

{% set function_name = create_function_heading(function) -%}
{{ create_heading(function_name, ".") }}

{{ print_description(function['briefdescription']) }}

{{ print_description(function['detaileddescription']) }}

{% endmacro -%}
{% set class = api[selector] %}

{{ create_class_heading(class, "=") }}

{% if class["scope"] is not none %}
**Scope:** {{ class["scope"] }}
{% endif %}

**In header:** {{ class["location"]["file"] }}

{% if class["briefdescription"] !=  []%}
Brief description
-----------------
{{class["briefdescription"]}}
{% endif %}

Member functions (public)
-------------------------

.. csv-table::
    :widths: auto

{% for member_selector in class["members"] -%}
{% set member = api[member_selector] %}
    {%- if member["type"] in ["function"] %}
    "{{member["return_type"]}}", "{{- create_function_signature(member_selector, member) }}"
    {%- endif -%}
{%- endfor %}

Description
-----------


Member Function Description
---------------------------

{% for member_selector in class["members"] -%}
{% set member = api[member_selector] %}
{{- create_function_description(member_selector, member) }}
{%- endfor %}
