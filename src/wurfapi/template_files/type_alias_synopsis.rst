{% import 'macros.rst' as macros with context -%}

{%- if api[selector]["kind"] == "typedef" or api[selector]["kind"] == "using" -%}
{%- set type_aliases = [selector] -%}
{%- else -%}
{%- set type_aliases = api[selector]["members"]  | api_filter(kind=["using", "typedef"])
                                             | api_sort(keys=["location", "line"])
                                             | api_sort(keys=["location", "path"]) -%}
{%- endif -%}

{%- if type_aliases|length > 1 -%}
{{ macros.format_type_alias_table(type_aliases) }}
-----

{% endif -%}

{% for type_alias in type_aliases -%}

{{ macros.format_type_alias(type_alias) }}

{% if api[type_alias]["scope"] %}
**Scope:** {{ api[type_alias]["scope"] }}
{% endif %}

{% if api[type_alias]["location"]["include"] %}
**In header:** ``#include <{{ api[type_alias]["location"]["include"] }}>``
{% endif %}

{{ "-----" if not loop.last }}

{% endfor %}
