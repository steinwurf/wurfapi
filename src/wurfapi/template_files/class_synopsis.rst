{%- macro create_heading(class, char='=') -%}
{%- set name = class["type"] + " " + class["name"] -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
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
{{ signature|join("") -}}
{%- endmacro -%}

{%- macro create_function_description(unique_name, function) -%}
{# First element is a label to the unique_name #}
.. _{{unique_name}}:

- {{function['return_type']}} {{ create_function_signature(unique_name, function)}}

{{function['briefdescription']}}
{{function['detaileddescription']}}

{% endmacro -%}
{% set class = api[selector] %}

{{ create_heading(class, "=") }}

{% if class["scope"] is not none %}
**Scope:** {{ class["scope"] }}
{% endif %}

**In header:** {{ class["location"]["file"] }}

{% if class["briefdescription"] != "" %}
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
