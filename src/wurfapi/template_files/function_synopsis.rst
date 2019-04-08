{% from 'macros.rst' import format_description %}
{% from 'macros.rst' import format_type_to_link %}
{% from 'macros.rst' import format_heading %}
{% from 'macros.rst' import format_function %}

{% set function = api[selector] %}

.. _{{selector}}:

{{ format_heading(function["kind"] + " " + function["name"], "-") }}

{% if function["scope"] %}
**Scope:** {{ function["scope"] }}
{% endif %}

**In header:** ``#include <{{ function["location"]["file"] }}> : function["location"]["line-start"]``

{{ format_function(api, selector) }}
