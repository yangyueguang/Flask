# coding=utf-8
from doc.document import Document


def sentry_test():
    import sentry_sdk
    DSN = 'https://0c0408449024425b8785a4177b4e443b@o427966.ingest.sentry.io/5372833'
    sentry_sdk.init(DSN)
    sentry_sdk.add_breadcrumb(
        message='I都发生了距离 cart',
        category='萨芬',
        data={
            'isbn': '978-可怜的撒',
            'dfa': '3'
        }
    )
    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message('大', '有意思')
    from raven import Client
    client = Client(DSN)
    try:
        1 / 0
    except:
        client.user_context({
            'user': 'youxiang邮箱',
            'data': '内容内容'
        })
        client.captureException()


if __name__ == '__main__':
    f = '/Users/supers/Desktop/company/a.pdf'
    result = Document.parse(f)
    print(result.text)





