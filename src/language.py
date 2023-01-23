#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import settings
from googletrans import Translator
from googletrans.models import Detected
import langdetect

logger = logging.getLogger(__name__)


def check_ru_chars(text):
    cyrrilic_ru = [
        "Ы", "ы",
        "Ё", "ё",
        "Э", "э",
        "Ъ", "ъ",
    ]
    detect_points = 0
    try:
        for c in cyrrilic_ru:
            result = text.find(str(c))
            if result != -1:
                detect_points += 1
        if detect_points >= 2:
            return "ru"
        else:
            return ""
    except Exception as Err:
        print(f"cyrrilic_ru: language detect error, {Err}")
        return ""


def check_by_google(text):
    try:
        translator = Translator()
        result = translator.detect(text)
        lang = result.lang
        match = result.confidence
        if match is None:
            return lang
        if match >= settings.google_match_threshold:
            return lang
        else:
            return ""
    except Exception as Err:
        print(f"googletrans: language detect error, {Err}")
        return ""


def check_by_langdetect(text):
    try:
        result = langdetect.detect(text)
        return str(result)
    except Exception as Err:
        print(f"langdetect: language detect error, {Err}")
        return ""


def is_lang(target_lang, text):
    detect_points = 0

    # Check by google
    lang = check_by_google(text)
    # print(f"google: {lang}")
    if lang == target_lang:
        detect_points += 1

    # Check by chars check
    lang = check_ru_chars(text)
    # print(f"chars: {lang}")
    if lang == target_lang:
        detect_points += 1

    # Check by langdetect
    lang = check_by_langdetect(text)
    # print(f"langdetect: {lang}")
    if lang == target_lang:
        detect_points += 1

    # print(f"Language: 'ru' points = {detect_points}")
    if detect_points >= 2:
        return True
