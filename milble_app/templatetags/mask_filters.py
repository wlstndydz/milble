from django import template

register = template.Library()

@register.filter(name='mask_author')
def mask_author(author):
    if len(author) > 1:
        return author[0] + '*' * (len(author) - 1)  # 첫 글자 제외한 나머지 '*'로 마스킹
    return author  # 한 글자일 경우 그대로 반환
