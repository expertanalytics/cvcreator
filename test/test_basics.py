import cvcreator as cv


def test_parse_partial_iterpolate():
    template = ["%(a)s\n%(b)s",
                {"a": "A:%s", "b": "B:%s"}]
    content = {"a": "hello"}
    assert cv.parse(content, template) == "A:hello\n"
