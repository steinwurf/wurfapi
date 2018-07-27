{% from 'macros.rst' import format_description %}

{# FORMAT_PARAMETERS #}

{%- macro format_parameters(parameters) -%}
(
{%- for parameter in parameters -%}
    {%- set type = parameter["type"] -%}
    {%- set name = parameter["name"] -%}
    {{type}} {{name}}{{ ", " if not loop.last }}
{%- endfor -%}
)
{%- endmacro -%}


{# FORMAT_RETURN #}

{%- macro format_return_description(description) -%}
{%- if description|length -%}
Returns:
    {{ format_description(description) | indent }}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_PARAMETER_DESCRIPTION #}

{%- macro format_parameter_description(parameter) -%}
{%- if parameter["description"] | length -%}
Parameter ``{{parameter["name"]}}``:
    {{ format_description(parameter["description"]) | indent }}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_PARAMETERS_DESCRIPTION #}

{%- macro format_parameters_description(parameters) -%}
{%- if parameters | length -%}
{% for parameter in parameters %}
{{ format_parameter_description(parameter)  }}
{% endfor %}
{%- endif -%}
{%- endmacro -%}


{# FORMAT_FUNCTION #}

{%- macro format_function(api, selector) -%}

.. _{{selector}}:

{% set return_type = api[selector]["return_type"] -%}
{%- set name = api[selector]["name"] -%}
{%- set briefdescription = api[selector]["briefdescription"] -%}
{%- set detaileddescription = api[selector]["detaileddescription"] -%}
{%- set parameters =
    format_parameters(api[selector]["parameters"]) -%}
{%- set return_description = api[selector]["return_description"] -%}

{{ return_type }} **{{ name }}** {{ parameters }}

    {{ format_description(briefdescription)|indent }}

    {{ format_description(detaileddescription)|indent }}

    {{ format_parameters_description(api[selector]["parameters"])|indent }}

    {{ format_return_description(return_description) | indent }}

{% endmacro -%}

