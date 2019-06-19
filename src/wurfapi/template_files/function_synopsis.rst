{%- from 'macros.rst' import format_description -%}
{%- from 'macros.rst' import format_type_list -%}
{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_function -%}

{%- set function = api[selector] -%}
{%- set parameters_out = [] -%}
{%- for parameter in function["parameters"] -%}
{%- do parameters_out.append(format_type_list(parameter["type"])) -%}
{%- if not loop.last -%}
{%- do parameters_out.append(", ") -%}
{%- endif -%}
{%- endfor -%}
{{ format_heading(function["kind"] + " " + function["name"] + "(" + parameters_out|join('') + ")", "-") }}

{% if function["scope"] %}
**Scope:** {{ function["scope"] }}
{% endif %}

{% if function["location"]["include"] %}
**In header:** ``#include <{{ function["location"]["include"] }}>``
{% endif %}

{{ format_function(api, selector) }}
