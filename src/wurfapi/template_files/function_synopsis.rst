{%- from 'macros.rst' import format_type_list -%}
{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_function -%}

{%- set function = api[selector] -%}
{%- set params = [] -%}
{%- for parameter in function["parameters"] -%}
{%- do params.append(format_type_list(parameter["type"])) -%}
{%- if not loop.last -%}
{%- do params.append(", ") -%}
{%- endif -%}
{%- endfor -%}
{{ format_heading(function["kind"] + " " + function["name"] + "(" + params|join('') + ")", "-") }}

{% if function["scope"] %}
**Scope:** {{ function["scope"] }}
{% endif %}

{% if function["location"]["include"] %}
**In header:** ``#include <{{ function["location"]["include"] }}>``
{% endif %}

{{ format_function(api, selector) }}
