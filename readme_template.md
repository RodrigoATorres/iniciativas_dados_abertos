{% for cat  in cat_names %} 
# {{cat}}
{% for info in all_info[cat] %}
## {{info['project_name']}}
{{info['url']}}

{{info['description']}}

:busts_in_silhouette: {{info['contributors']}} colaboradores
:star: {{info['stargazers']}} stars
:page_with_curl: {{info['commits']}} commits

:clock5: Último commit `{{info['last_commit'][:10]}}`

|{%- for lang_info in info['lang_percs'] -%}
{{lang_info[0]}}|
{%- endfor %}
|{%- for lang_info in info['lang_percs'] -%}
-|
{%- endfor %}
|{%- for lang_info in info['lang_percs'] -%}
![{{lang_info[1]}}%](https://progress-bar.dev/{{lang_info[1]}})|
{%- endfor %}

{% endfor %}
{% endfor %}
