import json
import os
import tempfile

import pytest

import contractions


def test_expand():
    assert contractions.expand("you're happy now") == "you are happy now"


def test_insensitivity():
    assert contractions.expand("You're happier now") == "You are happier now"


def test_add():
    contractions.add('mychange', 'my change')
    assert contractions.expand('mychange') == 'my change'


def test_add_dict():
    custom_dict = {
        'customone': 'custom one',
        'customtwo': 'custom two',
        'customthree': 'custom three',
        "can't": 'cannot',
        "won't": 'will not',
        "shouldn't": 'should not'
    }
    contractions.add_dict(custom_dict)

    assert contractions.expand('customone') == 'custom one'
    assert contractions.expand('customtwo') == 'custom two'
    assert contractions.expand('customthree') == 'custom three'
    assert contractions.expand('customone and customtwo') == 'custom one and custom two'

    assert contractions.expand('Customone') == 'Custom One'

    assert contractions.expand("can't") == 'cannot'
    assert contractions.expand("won't") == 'will not'
    assert contractions.expand("shouldn't") == 'should not'
    assert contractions.expand("Can't") == 'Cannot'


def test_ill():
    txt = 'He is to step down at the end of the week due to ill health'
    assert contractions.expand(txt) == txt
    assert contractions.expand("I'll") == "I will"


def test_preview():
    text = "This's a simple test including two sentences. I'd use it to test preview()."
    preview_items = contractions.preview(text, context_chars=10)
    print(preview_items)
    assert len(preview_items) == 2
    assert preview_items[0]['match'] == "This's"
    assert preview_items[1]['match'] == "I'd"
    assert text[preview_items[0]['start']: preview_items[0]['end']] == "This's"
    assert text[preview_items[1]['start']: preview_items[1]['end']] == "I'd"
    assert "This's" in preview_items[0]["viewing_window"]
    assert "I'd" in preview_items[1]["viewing_window"]
    text2 = ""
    preview_items2 = contractions.preview(text2, context_chars=10)
    assert preview_items2 == []


def test_preview_invalid_context_chars():
    text = "I'd like this"
    with pytest.raises(TypeError):
        contractions.preview(text, context_chars="ten")
    with pytest.raises(TypeError):
        contractions.preview(text, context_chars=10.5)


def test_empty_string():
    assert contractions.expand("") == ""


def test_no_contractions():
    text = "This is a simple sentence."
    assert contractions.expand(text) == text


def test_multiple_contractions():
    result = contractions.expand("I'm sure you're going to love what we've done")
    assert result == "I am sure you are going to love what we have done"


def test_case_preservation():
    assert contractions.expand("You're") == "You are"
    assert contractions.expand("YOU'RE") == "YOU ARE"
    assert contractions.expand("you're") == "you are"


def test_add_dict_empty():
    contractions.add_dict({})


def test_add_dict_overwrites():
    contractions.add_dict({"test123": "original"})
    assert contractions.expand("test123") == "original"
    contractions.add_dict({"test123": "updated"})
    assert contractions.expand("test123") == "updated"


def test_load_file():
    test_data = {
        "jsontest1": "json test one",
        "jsontest2": "json test two",
        "jsoncustom": "json custom"
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        contractions.load_file(temp_path)
        assert contractions.expand("jsontest1") == "json test one"
        assert contractions.expand("jsontest2") == "json test two"
        assert contractions.expand("jsoncustom") == "json custom"
    finally:
        os.unlink(temp_path)


def test_load_file_file_not_found():
    with pytest.raises(FileNotFoundError):
        contractions.load_file("/nonexistent/path/to/file.json")


def test_load_file_invalid_json():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            contractions.load_file(temp_path)
    finally:
        os.unlink(temp_path)


def test_load_file_non_dict():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(["not", "a", "dict"], f)
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="must contain a JSON dictionary"):
            contractions.load_file(temp_path)
    finally:
        os.unlink(temp_path)


def test_expand_leftovers_only():
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=True, slang=False)
    assert result == "I am happy you are here"


def test_expand_slang_only():
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=False, slang=True)
    assert result == "I am happy you are here"


def test_expand_basic_only():
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=False, slang=False)
    assert result == "I am happy you are here"


def test_expand_invalid_input():
    with pytest.raises(TypeError, match="text must be a string"):
        contractions.expand(None)
    with pytest.raises(TypeError, match="text must be a string"):
        contractions.expand(123)


def test_add_invalid_input():
    with pytest.raises(TypeError, match="contraction must be a string"):
        contractions.add(123, "test")
    with pytest.raises(TypeError, match="expansion must be a string"):
        contractions.add("test", 456)
    with pytest.raises(ValueError, match="contraction cannot be empty"):
        contractions.add("", "test")
    with pytest.raises(ValueError, match="expansion cannot be empty"):
        contractions.add("test", "")


def test_add_dict_invalid_input():
    with pytest.raises(TypeError, match="contractions_dict must be a dict"):
        contractions.add_dict("not a dict")
    with pytest.raises(TypeError, match="contractions_dict must be a dict"):
        contractions.add_dict(123)


def test_fix_deprecated_alias():
    with pytest.warns(DeprecationWarning, match="fix\\(\\) is deprecated.*Use expand\\(\\) instead"):
        result = contractions.fix("you're happy")
    assert result == "you are happy"


def test_shortcuts():
    assert contractions.e("you're") == "you are"
    preview_result = contractions.p("it's", 5)
    assert len(preview_result) == 1
    assert preview_result[0]["match"] == "it's"
