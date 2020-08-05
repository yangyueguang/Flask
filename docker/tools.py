# coding=utf-8
import numpy as np
import difflib
import copy
from itertools import chain
from doc.element import Catelog


def modify_text_box(text_box, modified_text):
    action_list = _compare_text(text_box.text, modified_text)
    for idx, action_type, action_data in action_list:
        if action_type == 'replace':
            old_char, new_char = action_data
            text_box.chars[idx].str = new_char
        elif action_type == 'pop':
            text_box.chars[idx].str = ' '
        elif action_type == 'insert':
            try:
                left_char = text_box.chars[idx - 1]
            except Exception as _:
                left_char = None
            try:
                right_char = text_box.chars[idx]  # if idx < len(text_box.chars) else None
            except Exception as _:
                right_char = None
            if right_char is not None:
                insert_char = copy.deepcopy(right_char)
            elif left_char is not None:
                insert_char = copy.deepcopy(left_char)
            else:
                continue
            insert_char.str = action_data
            insert_char.width = .1
            insert_char.offset = -1
            char_count = 0
            found_line_flag = False
            target_line = None
            char_index_in_line = 0
            for line in text_box.lines:
                if found_line_flag:
                    break
                for i, char in enumerate(line.chars):
                    if char_count == idx:
                        target_line = line
                        char_index_in_line = i
                        found_line_flag = True
                        break
                    char_count += 1
            if not found_line_flag:
                target_line = text_box.lines[-1]
                char_index_in_line = len(target_line.chars)
            target_line.insert_char(char_index_in_line, insert_char)


def _compare_text(source_text, target_text):
    sm = difflib.SequenceMatcher(None, source_text, target_text)
    action_list = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'insert':
            for char in target_text[j1:j2]:
                action = (i1, 'insert', char)
                action_list.append(action)
        elif tag == 'replace':
            source_chars = source_text[i1:i2]
            target_chars = target_text[j1:j2]
            if len(source_chars) > len(target_chars):
                for idx, char in enumerate(target_chars):
                    action = (idx + i1, 'replace', (source_chars[idx], char))
                    action_list.append(action)
                for idx in range(i1 + len(target_chars), i2):
                    action = (idx, 'pop', None)
                    action_list.append(action)
            else:
                for idx, char in enumerate(source_chars):
                    action = (idx + i1, 'replace', (char, target_chars[idx]))
                    action_list.append(action)
                for idx in range(len(source_chars), j2 - j1):
                    action = (i2, 'insert', target_chars[idx])
                    action_list.append(action)
        elif tag == 'delete':
            for idx in range(i1, i2):
                action = (idx, 'pop', None)
                action_list.append(action)
        else:
            pass
    action_list.reverse()
    return action_list


def detect_content(page_line_combined_data):
    contents_pages = []
    contents_chars = []
    for page, lines in sorted(page_line_combined_data.items(), key=lambda x: x[0]):
        line_list = [''.join(map(lambda x: x.str, chars)) for chars in lines]
        line_list = [line for line in line_list if line.strip()]
        dot_line_list = [line for line in line_list if '.' * 10 in line]
        if len(dot_line_list) / float(len(line_list) + 1) >= 0.33:
            contents_pages.append(page)
            contents_chars.extend([char for char in list(chain(*lines)) if char.type == 'paragraph'])
    if contents_chars:
        contents = Catelog(None, contents_chars)
        for node in contents.chars:
            node.type = 'contents'
        return contents





