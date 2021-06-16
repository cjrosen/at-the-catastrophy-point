
from book import Book, SvgRenderer, SvgPage

def test_page(svg, page, book, data):
    svg.text(page.x_content(0), page.y_content(100), data['text'], 'default')
    svg.text_box(page.x_content(0), page.y_content(100), book.px(64), book.px(48), data['text'], 'default')
    svg.image(page.x_content(0), page.y_content(0), book.px(64), book.px(48), data['frame'])

if __name__ == '__main__':
    book = Book(200, 220, 300)
    book.add_page(SvgPage('default', {
            'frame': '../original_frames/frame_0000.jpg',
            'text': "En text till olles bok."
        }, test_page), number=None)

    book.update()
    print(book)
    renderer = SvgRenderer()
    renderer.render_template(book, 'default')
    for page in book.pages:
        renderer.render_page(page, 'output/essvik', True)
    #book.render_page(0)

    print("main done")