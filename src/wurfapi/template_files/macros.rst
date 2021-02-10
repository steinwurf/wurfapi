{# FORMAT_CODE_BLOCK #}

{% macro format_code_block(paragraph) %}


.. code-block:: c++

{{ paragraph["content"] | indent(first=true) }}

{% endmacro %}


{# FORMAT_CODE_INLINE #}

{% macro format_code_inline(paragraph) %}
``{{ paragraph["content"] }}``
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
{{ content | replace('<', '\\<') | replace('>', '\\>') }}
{%- endmacro %}

{# FORMAT_REF

The escaped space is needed to that the inline markup ends with
a non-character. Otherwise rst will fail with an error.
#}

{% macro format_ref(content, reference) -%}
{% if api[reference]["kind"] == "file" -%}
`{{ api[reference]["path"] }}`
{%- else -%}
:ref:`{{ escape_ref(content) }} <{{ escape_ref(reference) }}>`{{"\\ "}}
{%- endif %}
{%- endmacro %}


{# FORMAT_LINK

The escaped space is needed to that the inline markup ends with
a non-character. Otherwise rst will fail with an error.
#}

{% macro format_link(content, link) %}
{% if link["url"] -%}
`{{ escape_ref(content) }} <{{ escape_ref(link["value"]) }}>`_{{"\\ "}}
{%- else -%}
{{ format_ref(content, link["value"]) }}
{%- endif %}
{% endmacro %}


{# FORMAT_TYPE_LIST #}

{% macro format_type_list(element, as_code=False) %}
{% for item in element %}
{% set value = item["value"] | replace('*', '\\*') %}
{% if "link" in item and not as_code %}
{{ format_link(value, item["link"]) -}}
{% else %}
{{ value -}}
{% endif %}
{% endfor %}
{% endmacro %}


{# FORMAT_TEXT #}

{% macro format_text(paragraph) %}
{% if "link" in paragraph %}
{{ format_link(paragraph["content"], paragraph["link"]) -}}
{% else %}
{{ paragraph["content"] -}}
{% endif %}
{% endmacro %}


{# FORMAT_LIST #}

{% macro format_list(list) %}
{% set item_type = "#. " if list["ordered"] else "- " %}
{% for item in list["items"] %}


{{ item_type }}{{format_paragraphs(item) | indent(width=item_type|length)}}
{%- endfor %}
{% endmacro %}


{# FORMAT_PARAGRAPHS #}

{% macro format_paragraphs(paragraphs) %}
{% for paragraph in paragraphs %}
{{format_paragraph(paragraph)}}
{% endfor %}
{% endmacro %}

{# FORMAT_PARAGRAPH #}

{% macro format_paragraph(paragraph) %}
{% for element in paragraph %}
{% if not loop.first %}
{% set last_element = paragraph[loop.index0 - 1] %}
{% set last_was_code_block = (last_element.kind == "code" and last_element.is_block) %}
{% set startswith_punctuation = 'content' in element and element.content[0] in ',.!?:;' %}
{%- if not startswith_punctuation and not last_was_code_block -%}
{{ " " -}}
{% endif %}
{% endif %}
{% if element["kind"] == "text" %}
{{ format_text(element) -}}
{% elif element["kind"] == "code" %}
{{ format_code(element) -}}
{% elif element["kind"] == "list" %}
{{ format_list(element) -}}
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
{{format_paragraphs(item["briefdescription"])}}
{%- endif -%}
{%- if item["detaileddescription"] -%}
{{format_paragraphs(item["detaileddescription"])}}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_PARAMETERS #}

{% macro format_parameters(parameters, as_code=False) -%}
(
{%- for parameter in parameters -%}
    {% set type = parameter["type"] %}
    {{- format_type_list(type, as_code=as_code) -}}
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

{% macro format_return_description(description) %}
{% if description|length %}
Returns:
    {{ format_paragraphs(description) | indent -}}
{% endif %}
{% endmacro %}


{# FORMAT_PARAMETER_DESCRIPTION #}

{% macro format_parameter_description(parameter) %}
{% if parameter["description"] | length %}
Parameter ``{{parameter["name"]}}``:
    {{ format_paragraphs(parameter["description"]) | indent }}

{% endif %}
{% endmacro %}

{# FORMAT_PARAMETERS_DESCRIPTION #}

{% macro format_parameters_description(parameters) %}
{% if parameters | length %}
{% for parameter in parameters %}
{% set description = format_parameter_description(parameter) %}
{% if description %}
{{ description }}
{% endif %}
{% endfor %}
{% endif %}
{% endmacro %}

{# FORMAT_TEMPLATE_PARAMETER_DESCRIPTION #}

{% macro format_template_parameter_description(parameter) %}
{% if "description" in parameter %}
{% set type = format_type_list(parameter["type"]) %}
{% set name = parameter["name"] %}
{% set default = format_type_list(parameter["default"]) | default("") %}
{% set description = format_paragraphs(parameter["description"]) %}
Template parameter: {{ type }} ``{{ name }}`` {{ " = " + default if default }}
    {{ description | indent -}}
{% endif %}
{% endmacro %}


{# FORMAT_TEMPLATE_PARAMETERS_DESCRIPTION #}

{% macro format_template_parameters_description(parameters) %}
{% if parameters | length %}
{% for parameter in parameters %}
{% set description = format_template_parameter_description(parameter) %}
{% if description %}
{{ description }}

{% endif %}
{% endfor %}
{% endif %}
{% endmacro %}

{# FORMAT_FUNCTION #}

{% macro format_function(selector, include_label=True) %}
{% set function = api[selector] %}
{% if include_label %}
.. wurfapitarget:: {{selector}}
{% if function["scope"] is not none %}
    :label: {{ function["scope"] }}::{{function["name"]}}()
{% else %}
    :label: {{function["name"]}}()
{%endif %}

{% endif %}
{% if "return" in function %}
{% set return_value = format_type_list(function["return"]["type"]) %}
{% set return_description =
    format_return_description(function["return"]["description"]) %}
{% endif %}
{% set name = function["name"] %}
{% set briefdescription = format_paragraphs(function["briefdescription"]) %}
{% set detaileddescription = format_paragraphs(function["detaileddescription"]) %}
{% set parameters =
    format_parameters(function["parameters"]) %}
{% set parameters_description =
    format_parameters_description(function["parameters"]) %}
{% if function["template_parameters"] %}
| template {{ format_template_parameters(function["template_parameters"]) }}
{% endif %}
{% if return_value is defined %}
{% if function["trailing_return"] %}
| auto **{{ name }}** {{ parameters }}{{" const" if function["is_const"] else ""}} -> {{ return_value }}
{% else %}
| {{ return_value }} **{{ name }}** {{ parameters }}{{" const" if function["is_const"] else ""}}
{% endif %}
{% else %}
| **{{ name }}** {{ parameters }}
{% endif %}
{% if briefdescription %}

    {{ briefdescription | indent }}
{% endif %}
{% if detaileddescription %}

    {{ detaileddescription | indent }}
{% endif %}
{% if parameters_description %}

    {{ parameters_description | indent }}
{% endif %}
{% if return_description %}

    {{ return_description | indent }}
{% endif %}
{% if function["template_parameters"] %}
{% set description =
    format_template_parameters_description(function["template_parameters"]) %}

    {{ description | indent -}}
{% endif %}
{% endmacro %}


{# FORMAT_FUNCTION_TABLE_ROW #}

{%- macro format_function_table_row(selector) -%}
{%- set function = api[selector] %}
{%- set signature = format_parameters(function["parameters"]) %}
{%- set signature = signature + " const" if function["is_const"] else signature -%}
{% if "return" in function -%}
{%- set return_type = format_type_list(function["return"]["type"]) -%}
{% else %}
{%- set return_type = "" -%}
{%- endif %}
{%- set return_type = "virtual " + return_type if function["is_virtual"] else return_type -%}
* - {{ return_type }}
  - {{ format_ref(function["name"], selector)}} {{ signature }}
{% endmacro -%}


{# FORMAT_FUNCTION_TABLE #}

{%- macro format_function_table(selectors) -%}
.. list-table::
   :header-rows: 0
   :widths: auto
   :align: left

{% for selector in selectors | api_sort(keys=["location", "line"])
                             | api_sort(keys=["location", "path"]) %}
   {{ format_function_table_row(selector) | indent(width=3) }}
{%- endfor -%}

{% endmacro -%}
