import json

import contractions


def test_fix():
    assert contractions.fix("you're happy now") == "you are happy now"


def test_insensitivity():
    assert contractions.fix("You're happier now") == "You are happier now"


def test_add():
    contractions.add('mychange', 'my change')
    assert contractions.fix('mychange') == 'my change'


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

    assert contractions.fix('customone') == 'custom one'
    assert contractions.fix('customtwo') == 'custom two'
    assert contractions.fix('customthree') == 'custom three'
    assert contractions.fix('customone and customtwo') == 'custom one and custom two'

    assert contractions.fix('Customone') == 'Custom One'

    assert contractions.fix("can't") == 'cannot'
    assert contractions.fix("won't") == 'will not'
    assert contractions.fix("shouldn't") == 'should not'
    assert contractions.fix("Can't") == 'Cannot'


def test_ill():
    txt = 'He is to step down at the end of the week due to ill health'
    assert contractions.fix(txt) == txt
    assert contractions.fix("I'll") == "I will"


def test_preview():
    text = "This's a simple test including two sentences. I'd use it to test preview()."
    preview_items = contractions.preview(text, flank=10)
    print(preview_items)
    assert len(preview_items) == 2
    assert preview_items[0]['match'] == "This's"
    assert preview_items[1]['match'] == "I'd"
    assert text[preview_items[0]['start']: preview_items[0]['end']] == "This's"
    assert text[preview_items[1]['start']: preview_items[1]['end']] == "I'd"
    assert "This's" in preview_items[0]["viewing_window"]
    assert "I'd" in preview_items[1]["viewing_window"]
    text2 = ""
    preview_items2 = contractions.preview(text2, flank=10)
    assert preview_items2 == []


def test_preview_invalid_flank():
    import pytest
    text = "I'd like this"
    with pytest.raises(TypeError):
        contractions.preview(text, flank="ten")
    with pytest.raises(TypeError):
        contractions.preview(text, flank=10.5)


def test_empty_string():
    assert contractions.fix("") == ""


def test_no_contractions():
    text = "This is a simple sentence."
    assert contractions.fix(text) == text


def test_multiple_contractions():
    result = contractions.fix("I'm sure you're going to love what we've done")
    assert result == "I am sure you are going to love what we have done"


def test_case_preservation():
    assert contractions.fix("You're") == "You are"
    assert contractions.fix("YOU'RE") == "YOU ARE"
    assert contractions.fix("you're") == "you are"


def test_add_dict_empty():
    contractions.add_dict({})


def test_add_dict_overwrites():
    contractions.add_dict({"test123": "original"})
    assert contractions.fix("test123") == "original"
    contractions.add_dict({"test123": "updated"})
    assert contractions.fix("test123") == "updated"


def test_load_json():
    import os
    import tempfile

    test_data = {
        "jsontest1": "json test one",
        "jsontest2": "json test two",
        "jsoncustom": "json custom"
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        contractions.load_json(temp_path)
        assert contractions.fix("jsontest1") == "json test one"
        assert contractions.fix("jsontest2") == "json test two"
        assert contractions.fix("jsoncustom") == "json custom"
    finally:
        os.unlink(temp_path)


def test_load_json_file_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        contractions.load_json("/nonexistent/path/to/file.json")


def test_load_json_invalid_json():
    import os
    import tempfile

    import pytest

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            contractions.load_json(temp_path)
    finally:
        os.unlink(temp_path)
