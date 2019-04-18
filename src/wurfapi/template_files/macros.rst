
{# FORMAT_CODE_BLOCK #}

{% macro format_code_block(paragraph) %}


.. code-block:: c++

{{ paragraph["content"] | indent(first=true) }}

{% endmacro %}


{# FORMAT_CODE_INLINE #}

{% macro format_code_inline(paragraph) %}
``{{ paragraph["content"] }}``{{ " " }}
{%- endmacro %}


{# FORMAT_CODE #}

{% macro format_code(paragraph) %}
{% if paragraph["is_block"] %}
{{ format_code_block(paragraph) }}
{%- else %}
{{ format_code_inline(paragraph) }}
{%- endif %}
{% endmacro %}


{# ESCAPE_REF #}

{% macro escape_ref(content) -%}
{{ content | replace('<', '\<') | replace('>', '\>') }}
{%- endmacro %}

{# FORMAT_REF #}

{% macro format_ref(content, reference) -%}
:ref:`{{ escape_ref(content) }} <{{ escape_ref(reference)  }}>`
{%- endmacro %}


{# FORMAT_LINK #}

{% macro format_link(content, link) %}
{% if link["url"] -%}
`{{ escape_ref(content) }} <{{ escape_ref(link["value"]) }}>`_
{%- else -%}
{{ format_ref(content, link["value"]) }}
{%- endif %}
{% endmacro %}


{# FORMAT_TYPE_LIST #}

{% macro format_type_list(element, as_code=False) %}
{% for item in element %}
{% set value = item["value"] | replace('*', '\*') %}
{% if "link" in item and not as_code %}
{{ format_link(value, item["link"]) -}}
{% else %}
{{ value -}}
{% endif %}
{{ " " if not loop.last -}}
{% endfor %}
{% endmacro %}


{# FORMAT_TEXT #}

{% macro format_text(paragraph) %}
{% if "link" in paragraph -%}
{{ format_link(paragraph["content"], paragraph["link"]) }}
{%- else -%}
{{ paragraph["content"] }}
{%- endif -%}
{{ " " }}
{%- endmacro %}


{# FORMAT_LIST #}

{% macro format_list(list) %}
{% set item_type = "#. " if list["ordered"] else "- " %}
{% for item in list["items"] %}


{{ item_type }}{{format_description(item) | indent(width=item_type|length)}}

{% endfor %}
{% endmacro %}


{# FORMAT_DESCRIPTION #}

{% macro format_description(description) %}
{% for para in description %}
{% if para["kind"] == "text" %}
{{ format_text(para) }}
{%- endif %}
{% if para["kind"] == "code" %}
{{ format_code(para) }}
{%- endif %}
{% if para["kind"] == "list" %}
{{ format_list(para) }}
{% endif %}
{% endfor %}
{% endmacro %}

{# FORMAT_HEADING #}

{%- macro format_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}


{# FORMAT_TYPEDEF_ALIAS #}

{%- macro format_typedef_alias(alias) -%}
typedef {{ format_type_list(alias["type"]) }} **{{ alias["name"] }}**
{%- endmacro -%}


{# FORMAT_USING_ALIAS #}

{%- macro format_using_alias(alias) -%}
using **{{ alias["name"] }}** = {{ format_type_list(alias["type"]) }}
{%- endmacro -%}


{# FORMAT_TYPE_ALIAS #}

{%- macro format_type_alias(alias) -%}
{%- if alias["kind"] == "using" -%}
    {{ format_using_alias(alias) }}
{%- else -%}
    {{ format_typedef_alias(alias) }}
{%- endif -%}
{%- endmacro -%}

{# MERGE_DESCRIPTION #}
{%- macro merge_description(item) -%}
{%- if item["briefdescription"] -%}
{{format_description(item["briefdescription"])}}
{%- endif -%}
{%- if item["detaileddescription"] -%}
{{format_description(item["detaileddescription"])}}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_PARAMETERS #}

{% macro format_parameters(parameters) -%}
(
{%- for parameter in parameters -%}
    {% set type = parameter["type"] %}
    {% set name = parameter["name"] %}
    {{- format_type_list(type) + " " -}}
    {% if name %}
    {{- name -}}
    {% endif %}
    {{- ", " if not loop.last -}}
{% endfor -%}
)
{%- endmacro -%}


{# FORMAT_TEMPLATE_PARAMETERS #}

{% macro format_template_parameters(parameters, as_code=False) -%}
<
{%- for parameter in parameters %}
    {% set type = parameter["type"] %}
    {% set name = parameter["name"] %}
    {{- format_type_list(type, as_code=as_code) + " " -}}
    {% if name %}
    {{- name -}}
    {% endif %}
    {% if "default" in parameter %}
    {{- " = " + format_type_list(parameter["default"], as_code=as_code) -}}
    {% endif %}
    {{- ", " if not loop.last -}}
{% endfor %}
>
{%- endmacro %}


{# FORMAT_RETURN #}

{%- macro format_return_description(description) -%}
{%- if description|length -%}
Returns:
    {{ format_description(description) | indent }}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_PARAMETER_DESCRIPTION #}

{% macro format_parameter_description(parameter) %}
{% if parameter["description"] | length %}
Parameter ``{{parameter["name"]}}``:
    {{ format_description(parameter["description"]) | indent }}

{% endif %}
{% endmacro %}


{# FORMAT_PARAMETERS_DESCRIPTION #}

{%- macro format_parameters_description(parameters) -%}
{%- if parameters | length -%}
{% for parameter in parameters %}
{{ format_parameter_description(parameter)  }}
{% endfor %}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_FUNCTION #}

{%- macro format_function(api, selector, include_label=True) -%}
{% if include_label %}
.. _{{selector}}:

{% endif %}
{% set return_value = api[selector]["return"] %}
{% set name = api[selector]["name"] %}
{% set briefdescription = api[selector]["briefdescription"] %}
{% set detaileddescription = api[selector]["detaileddescription"] %}
{% set parameters =
    format_parameters(api[selector]["parameters"]) %}
{% set return_description = api[selector]["return"]["description"] %}
{% if api[selector]["template_parameters"] %}
| template {{ format_template_parameters(api[selector]["template_parameters"]) }}
{% endif %}
| {{ format_type_list(return_value["type"]) }} **{{ name }}** {{ parameters }}

    {{ format_description(briefdescription)|indent }}

    {{ format_description(detaileddescription)|indent }}

    {{ format_parameters_description(api[selector]["parameters"])|indent }}

    {{ format_return_description(return_description) | indent }}

{% endmacro %}
