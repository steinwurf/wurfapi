
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


{%- macro cppreference_link(element) -%}
{%- set cppreference_map = dict() -%}
{%- do cppreference_map.update({'void': "keyword/void"}) -%}
{%- do cppreference_map.update({'bool': "keyword/bool"}) -%}
{%- do cppreference_map.update({'short': "keyword/short"}) -%}
{%- do cppreference_map.update({'int': "keyword/int"}) -%}
{%- do cppreference_map.update({'long': "keyword/long"}) -%}
{%- do cppreference_map.update({'float': "keyword/float"}) -%}
{%- do cppreference_map.update({'double': "keyword/double"}) -%}
{%- do cppreference_map.update({'std::vector': "container/vector"}) -%}
{%- do cppreference_map.update({'std::string': "string/basic_string"}) -%}
{%- do cppreference_map.update({'uint8_t': "types/integer"}) -%}
{%- do cppreference_map.update({'uint16_t': "types/integer"}) -%}
{%- do cppreference_map.update({'uint32_t': "types/integer"}) -%}
{%- do cppreference_map.update({'uint64_t': "types/integer"}) -%}
{%- do cppreference_map.update({'int8_t': "types/integer"}) -%}
{%- do cppreference_map.update({'int16_t': "types/integer"}) -%}
{%- do cppreference_map.update({'int32_t': "types/integer"}) -%}
{%- do cppreference_map.update({'int64_t': "types/integer"}) -%}
{%- set type = element["type"] -%}
{%- if type in cppreference_map -%}
{%- set page = cppreference_map.get(type) -%}
`{{type}} <http://en.cppreference.com/w/cpp/{{page}}>`_
{%- else -%}
{{type}}
{%- endif -%}
{%- endmacro -%}

{# FORMAT_TYPE_TO_LINK #}
{%- macro format_type_to_link(element) -%}
{%- if element["link"] -%}
:ref:`{{ element["type"] }}<{{ element["link"] }}>`
{%- else -%}
{{cppreference_link(element)}}
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
    {%- if para["type"] == "text" -%}
        {{ format_text(para) }}
    {%- endif -%}
    {%- if para["type"] == "code" -%}
        {{ format_code(para) }}
    {%- endif -%}
    {%- if para["type"] == "list" -%}
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
typedef {{ format_type_to_link(alias["identifier"]) }} **{{ alias["name"] }}**
{%- endmacro -%}


{# FORMAT_USING_ALIAS #}

{%- macro format_using_alias(alias) -%}
using **{{ alias["name"] }}** = {{ format_type_to_link(alias["identifier"]) }}
{%- endmacro -%}


{# FORMAT_TYPE_ALIAS #}

{%- macro format_type_alias(alias) -%}
{%- if alias["type"] == "using" -%}
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
