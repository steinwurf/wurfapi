
{# FORMAT_CODE_BLOCK #}

{%- macro format_code_block(paragraph) %}

.. code-block:: c++

{{ paragraph["content"] | indent(first=true) }}

{% endmacro -%}


{# FORMAT_CODE_INLINE #}

{%- macro format_code_inline(paragraph) -%}
``{{ paragraph["content"] }}``{{ " " }}
{%- endmacro -%}


{# FORMAT_CODE #}

{%- macro format_code(paragraph) -%}
{%- if paragraph["is_block"] -%}
    {{ format_code_block(paragraph) }}
{%- else -%}
    {{ format_code_inline(paragraph) }}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_TYPE_TO_LINK #}
{%- macro format_type_to_link(element) -%}
{%- if element["link"] -%}
:ref:`{{ element["type"] }}<{{ element["link"] }}>`
{%- else -%}
{{ element["type"] }}
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


{# FORMAT_LIST #}

{%- macro format_list(list) -%}
{%- set item_type = "#. " if list["ordered"] else "- " %}
{% for item in list["items"] %}
{{ item_type }}{{format_description(item) | indent(width=item_type|length)}}
{%- endfor %}

{%- endmacro -%}


{# FORMAT_DESCRIPTION #}

{%- macro format_description(description) -%}
{%- for para in description -%}
    {%- if para["kind"] == "text" -%}
        {{ format_text(para) }}
    {%- endif -%}
    {%- if para["kind"] == "code" -%}
        {{ format_code(para) }}
    {%- endif -%}
    {%- if para["kind"] == "list" -%}
        {{ format_list(para) }}
    {%- endif -%}
{%- endfor -%}
{%- endmacro -%}

{# FORMAT_HEADING #}

{%- macro format_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}


{# FORMAT_TYPEDEF_ALIAS #}

{%- macro format_typedef_alias(alias) -%}
typedef {{ format_type_to_link(alias["type"]) }} **{{ alias["name"] }}**
{%- endmacro -%}


{# FORMAT_USING_ALIAS #}

{%- macro format_using_alias(alias) -%}
using **{{ alias["name"] }}** = {{ format_type_to_link(alias["type"]) }}
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
