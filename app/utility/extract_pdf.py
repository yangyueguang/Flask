# coding=utf-8
# email:  younixiao@qq.com
# create: 2020年6月28日星期日 14:13

import fitz

def extract_pdf(file_name):
    document = fitz.open(file_name)

    base_index = 0
    result = {
        'page_infos': {},
        'pages': {},
        'contents': {},
        'text': ''
    }
    chars = []

    for page_number in range(document.pageCount):
        page_json = {
            'baseIndex': base_index
        }
        page = document.loadPage(page_number)
        page_raw = page.getDisplayList().getTextPage().extractRAWDICT()
        page_json['info'] = {
            'num': page_number + 1,
            'scale': 1,
            'rotation': page.rotation,
            'offsetX': 0,
            'offsetY': 0,
            'width': page_raw['width'],
            'height': page_raw['height']
        }
        page_json['content'] = []
        for block in page_raw['blocks']:
            for line in block['lines']:
                for span in line['spans']:
                    for char in span['chars']:
                        # x0, y0, x1, y1 = char['bbox']
                        x0, y0 = char['origin']
                        c = char['c']
                        base_index += 1
                        page_json['content'].append({
                            'char': c,
                            'x': x0,
                            'y': y0,
                            'width': span['size'],
                            'height': span['size'],
                            'str': c,
                            'fontName': span['font']
                        })
                        chars.append(c)
        page_info = page_json['info']
        page_info['pageCharsCount'] = len(page_json['content'])
        result['page_infos'][page_number + 1] = page_info
        result['pages'][page_number + 1] = page_json
        result['contents'][page_number + 1] = page_json['content']
    result['text'] = ''.join(chars)
    return result

