
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


{# FORMAT_DESCRIPTION #}

{%- macro format_description(description) -%}
{%- for para in description -%}
    {%- if para["type"] == "text" -%}
        {{ format_text(para) }}
    {%- endif -%}
    {%- if para["type"] == "code" -%}
        {{ format_code(para) }}
    {%- endif -%}
{%- endfor -%}
{%- endmacro -%}

{# FORMAT_HEADING #}

{%- macro format_heading(name, char='=') -%}
{%- set size = name|length -%}
{{name}}
{% for n in range(size) %}{{char}}{% endfor %}
{%- endmacro -%}
