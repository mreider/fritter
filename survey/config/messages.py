# -*- coding: utf-8 -*-

MESSAGES = {
}

def get_message(key, **kwargs):
    template, code = MESSAGES.get(key, None)

    if not template:
        return key

    context = dict((key,value) for key,value in kwargs.items() if '{{{k}}}'.format(k=key) in template)

    return template.format(**context), code
