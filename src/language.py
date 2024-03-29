#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import settings
from granslate import Translator
import asyncio
import langdetect

import nest_asyncio
nest_asyncio.apply()

logger = logging.getLogger(__name__)


def check_ru_chars(text):
    cyrrilic_ru = [
        "Ы", "ы",
        "Ё", "ё",
        "Э", "э",
        "Ъ", "ъ",
    ]
    matches = 0
    try:
        for c in cyrrilic_ru:
            count = len(re.findall(c, text))
            result = text.find(str(c))
            if result != -1:
                matches += count
        if matches >= 2:
            return "ru"
        else:
            return ""
    except Exception as Err:
        print(f"cyrrilic_ru: language detect error, {Err}")
        return ""


def check_by_google(text):
    try:
        translator = Translator()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(translator.detect(text))
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
