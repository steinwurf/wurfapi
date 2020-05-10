{%- from 'macros.rst' import format_heading -%}
{%- from 'macros.rst' import format_paragraphs -%}
{%- from 'macros.rst' import merge_description -%}

{{ format_heading("Macros") }}

{% set macros = api | api_filter(kind="macro") %}

{{ macros }}
