{% import 'macros.rst' as macros with context -%}

{%- set function = api[selector] -%}
{%- set params = [] -%}
{%- for parameter in function["parameters"] -%}
{%- do params.append(macros.format_type_list(parameter["type"])) -%}
{%- if not loop.last -%}
{%- do params.append(", ") -%}
{%- endif -%}
{%- endfor -%}
{{ macros.format_heading(function["kind"] + " " + function["name"] + "(" + params|join('') + ")", "-") }}

{% if function["scope"] %}
**Scope:** {{ function["scope"] }}
{% endif %}

{% if function["location"]["include"] %}
**In header:** ``#include <{{ function["location"]["include"] }}>``
{% endif %}

{{ macros.format_function(selector) }}
