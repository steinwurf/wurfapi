{% import 'macros.rst' as macros with context -%}

{%- if api[selector]["kind"] == "function" -%}
{%- set functions = [selector] -%}
{%- else -%}
{%- set functions = api[selector]["members"] | api_filter(kind="function")
                                             | api_sort(keys=["location", "line"])
                                             | api_sort(keys=["location", "path"]) -%}
{%- endif -%}

{%- if functions|length > 1 -%}
{{ macros.format_function_table(functions) }}
-----

{% endif -%}

{% for function in functions -%}

{{ macros.format_function(function) }}

{% if api[function]["scope"] %}
**Scope:** {{ api[function]["scope"] }}
{% endif %}

{% if api[function]["location"]["include"] %}
**In header:** ``#include <{{ api[function]["location"]["include"] }}>``
{% endif %}

{{ "-----" if not loop.last }}

{% endfor %}