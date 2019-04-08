{%- from 'macros.rst' import format_description -%}
{%- from 'macros.rst' import format_type_to_link -%}
{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_function -%}
{%- set function = api[selector] -%}
{%- for parameter in parameters -%}
    {%- set type = parameter["type"] -%}
    {{ format_type_to_link(parameter) }}{{ ", " if not loop.last }}
{%- endfor -%}
{{ format_heading(function["kind"] + " " + function["name"] + "(" + function["parameters"]|map(attribute='type')|join(', ') + ")", "-") }}

{% if function["scope"] %}
**Scope:** {{ function["scope"] }}
{% endif %}

**In header:** ``#include <{{ function["location"]["file"] }}>``

{{ format_function(api, selector) }}
