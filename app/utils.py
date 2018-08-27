# -*- coding: utf-8

from transliterate import translit


def rutranslit(string):
    return translit(string, 'ru', reversed=True)
