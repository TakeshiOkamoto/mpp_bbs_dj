# --------------------------
#  (共通)カスタムフィルタ
# --------------------------
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

# スペース、タブを「&nbsp;」に変換する
@register.filter(name='nbsp')
def nbsp(value):
    # RAWになるのでhtmlspecialchars()と同様の処理も付加
    value = value.replace('&', '&amp;') \
                 .replace('"', '&quot;') \
                 .replace('\'', '&#039;') \
                 .replace('<', '&lt;') \
                 .replace('>', '&gt;') \
                 .replace(' ', '&nbsp;') \
                 .replace('	', '&nbsp;&nbsp;')
    return mark_safe(value)    