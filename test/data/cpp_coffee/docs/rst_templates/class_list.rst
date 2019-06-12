
{% set classes = api[selector]["members"] | api_filter(
       kind="class")
%}

{% for class in classes %}
* class {{ api[class]["name"] }}
{% endfor %}


