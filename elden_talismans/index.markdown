---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home    
---

# List of talismans in Elden Ring

{% for talisman in site.talismans %}

* ### [{{talisman.name}}]({{site.baseurl}}/{{talisman.url}})
{{talisman.desc}}



{% endfor %}