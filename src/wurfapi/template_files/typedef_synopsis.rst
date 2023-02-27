{% import 'macros.rst' as macros with context -%}

{%- if api[selector]["kind"] == "typedef" or api[selector]["kind"] == "using" -%}
{%- set typedefs = [selector] -%}
{%- else -%}
{%- set typedefs = api[selector]["members"]  | api_filter(kind=["using", "typedef"])
                                             | api_sort(keys=["location", "line"])
                                             | api_sort(keys=["location", "path"]) -%}
{%- endif -%}

{%- if typedefs|length > 1 -%}
{{ macros.format_typedef_table(typedefs) }}
-----

{% endif -%}

{% for typedef in typedefs -%}

{{ macros.format_type_alias(typedef) }}

{% if api[typedef]["scope"] %}
**Scope:** {{ api[typedef]["scope"] }}
{% endif %}

{% if api[typedef]["location"]["include"] %}
**In header:** ``#include <{{ api[typedef]["location"]["include"] }}>``
{% endif %}

{{ "-----" if not loop.last }}

{% endfor %}
