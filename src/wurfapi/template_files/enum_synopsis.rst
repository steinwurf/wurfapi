{% from 'macros.rst' import format_heading %}

{% set enum = api[selector] %}

.. _{{selector}}:

{{ format_heading("`enum` " + enum["name"]) }}
