{% set scope = selector.split('::') -%}
{% for s in scope -%}
{{s}}
{% endfor -%}
