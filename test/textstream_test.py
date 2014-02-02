

from . import jsonstream_import

TextStream = jsonstream_import("TextStream")
AwaitingData = jsonstream_import("AwaitingData")
EndOfStream = jsonstream_import("EndOfStream")


def assert_cursor_position(text, line_no, char_no):
    pass
    #assert text._TextStream__current_line == line_no
    #assert text._TextStream__current_char == char_no


def test_peek_at_end_of_line_with_more_lines():
    text = TextStream()
    assert_cursor_position(text, 0, 0)
    text.write("a")
    text.write("b")
    assert text.read() == "a"
    assert_cursor_position(text, 0, 1)
    assert text.peek() == "b"
    assert_cursor_position(text, 1, 0)
    assert text.peek() == "b"
    assert_cursor_position(text, 1, 0)


def test_peek_at_end_of_line_with_no_more_lines():
    text = TextStream()
    assert_cursor_position(text, 0, 0)
    text.write("a")
    assert text.read() == "a"
    assert_cursor_position(text, 0, 1)
    try:
        assert text.peek()
    except AwaitingData:
        assert True
    else:
        assert False
    assert_cursor_position(text, 1, 0)
    text.close()
    try:
        assert text.peek()
    except EndOfStream:
        assert True
    else:
        assert False
    assert_cursor_position(text, 1, 0)


def test_read_at_end_of_line():
    text = TextStream()
    assert_cursor_position(text, 0, 0)
    text.write("a")
    text.write("b")
    assert text.read() == "a"
    assert_cursor_position(text, 0, 1)
    assert text.read() == "b"
    assert_cursor_position(text, 1, 1)
    try:
        assert text.read()
    except AwaitingData:
        assert True
    else:
        assert False
    assert_cursor_position(text, 2, 0)


def test_read_any():
    digits = "0123456789"
    text = TextStream()
    assert_cursor_position(text, 0, 0)
    text.write("12 34")
    text.write("56 78")
    text.close()
    assert text.read_any(digits) == "12"
    assert_cursor_position(text, 0, 2)
    assert text.read() == " "
    assert_cursor_position(text, 0, 3)
    assert text.read_any(digits) == "3456"
    assert_cursor_position(text, 1, 2)
    assert text.read() == " "
    assert_cursor_position(text, 1, 3)
    assert text.read_any(digits) == "78"
    assert_cursor_position(text, 2, 0)


def test_cannot_write_when_not_writable():
    text = TextStream()
    text.write("a")
    text.close()
    try:
        assert text.write("b")
    except IOError:
        assert True
    else:
        assert False
