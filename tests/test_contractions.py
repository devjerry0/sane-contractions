import json
import os
import tempfile

import pytest

import contractions


def test_expand() -> None:
    assert contractions.expand("you're happy now") == "you are happy now"


def test_insensitivity() -> None:
    assert contractions.expand("You're happier now") == "You are happier now"


def test_add() -> None:
    contractions.add("mychange", "my change")
    assert contractions.expand("mychange") == "my change"


def test_add_dict() -> None:
    custom_dict = {
        "customone": "custom one",
        "customtwo": "custom two",
        "customthree": "custom three",
        "can't": "cannot",
        "won't": "will not",
        "shouldn't": "should not"
    }
    contractions.add_dict(custom_dict)

    assert contractions.expand("customone") == "custom one"
    assert contractions.expand("customtwo") == "custom two"
    assert contractions.expand("customthree") == "custom three"
    assert contractions.expand("customone and customtwo") == "custom one and custom two"

    assert contractions.expand("Customone") == "Custom One"

    assert contractions.expand("can't") == "cannot"
    assert contractions.expand("won't") == "will not"
    assert contractions.expand("shouldn't") == "should not"
    assert contractions.expand("Can't") == "Cannot"


def test_ill() -> None:
    txt = "He is to step down at the end of the week due to ill health"
    assert contractions.expand(txt) == txt
    assert contractions.expand("I'll") == "I will"


def test_preview() -> None:
    text = "This's a simple test including two sentences. I'd use it to test preview()."
    preview_items = contractions.preview(text, context_chars=10)
    print(preview_items)
    assert len(preview_items) == 2
    assert preview_items[0]["match"] == "This's"
    assert preview_items[1]["match"] == "I'd"
    
    start0 = preview_items[0]["start"]
    end0 = preview_items[0]["end"]
    start1 = preview_items[1]["start"]
    end1 = preview_items[1]["end"]
    assert isinstance(start0, int)
    assert isinstance(end0, int)
    assert isinstance(start1, int)
    assert isinstance(end1, int)
    assert text[start0:end0] == "This's"
    assert text[start1:end1] == "I'd"
    
    viewing_window0 = preview_items[0]["viewing_window"]
    viewing_window1 = preview_items[1]["viewing_window"]
    assert isinstance(viewing_window0, str)
    assert isinstance(viewing_window1, str)
    assert "This's" in viewing_window0
    assert "I'd" in viewing_window1
    
    text2 = ""
    preview_items2 = contractions.preview(text2, context_chars=10)
    assert preview_items2 == []


def test_preview_invalid_context_chars() -> None:
    text = "I'd like this"
    with pytest.raises(TypeError):
        contractions.preview(text, context_chars="ten")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        contractions.preview(text, context_chars=10.5)  # type: ignore[arg-type]


def test_empty_string() -> None:
    assert contractions.expand("") == ""


def test_no_contractions() -> None:
    text = "This is a simple sentence."
    assert contractions.expand(text) == text


def test_multiple_contractions() -> None:
    result = contractions.expand("I'm sure you're going to love what we've done")
    assert result == "I am sure you are going to love what we have done"


def test_case_preservation() -> None:
    assert contractions.expand("You're") == "You are"
    assert contractions.expand("YOU'RE") == "YOU ARE"
    assert contractions.expand("you're") == "you are"


def test_add_dict_empty() -> None:
    contractions.add_dict({})


def test_add_dict_overwrites() -> None:
    contractions.add_dict({"test123": "original"})
    assert contractions.expand("test123") == "original"
    contractions.add_dict({"test123": "updated"})
    assert contractions.expand("test123") == "updated"


def test_load_file() -> None:
    test_data = {
        "jsontest1": "json test one",
        "jsontest2": "json test two",
        "jsoncustom": "json custom"
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        contractions.load_file(temp_path)
        assert contractions.expand("jsontest1") == "json test one"
        assert contractions.expand("jsontest2") == "json test two"
        assert contractions.expand("jsoncustom") == "json custom"
    finally:
        os.unlink(temp_path)


def test_load_file_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        contractions.load_file("/nonexistent/path/to/file.json")


def test_load_file_invalid_json() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            contractions.load_file(temp_path)
    finally:
        os.unlink(temp_path)


def test_load_file_non_dict() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(["not", "a", "dict"], f)
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="must contain a JSON dictionary"):
            contractions.load_file(temp_path)
    finally:
        os.unlink(temp_path)


def test_load_folder() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "dict1.json")
        file2 = os.path.join(temp_dir, "dict2.json")
        
        with open(file1, "w", encoding="utf-8") as f:
            json.dump({"foldertest1": "folder test one", "foldertest2": "folder test two"}, f)
        
        with open(file2, "w", encoding="utf-8") as f:
            json.dump({"foldertest3": "folder test three"}, f)
        
        contractions.load_folder(temp_dir)
        
        assert contractions.expand("foldertest1") == "folder test one"
        assert contractions.expand("foldertest2") == "folder test two"
        assert contractions.expand("foldertest3") == "folder test three"


def test_load_folder_ignores_non_json() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        json_file = os.path.join(temp_dir, "valid.json")
        txt_file = os.path.join(temp_dir, "ignored.txt")
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({"validkey": "valid value"}, f)
        
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("this should be ignored")
        
        contractions.load_folder(temp_dir)
        assert contractions.expand("validkey") == "valid value"


def test_load_folder_not_found() -> None:
    with pytest.raises(FileNotFoundError, match="Folder not found"):
        contractions.load_folder("/nonexistent/folder/path")


def test_load_folder_not_directory() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"test": "data"}, f)
        temp_path = f.name
    
    try:
        with pytest.raises(NotADirectoryError, match="not a directory"):
            contractions.load_folder(temp_path)
    finally:
        os.unlink(temp_path)


def test_load_folder_no_json_files() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        txt_file = os.path.join(temp_dir, "file.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("no json here")
        
        with pytest.raises(ValueError, match="No JSON files found"):
            contractions.load_folder(temp_dir)


def test_expand_leftovers_only() -> None:
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=True, slang=False)
    assert result == "I am happy you are here"


def test_expand_slang_only() -> None:
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=False, slang=True)
    assert result == "I am happy you are here"


def test_expand_basic_only() -> None:
    text = "I'm happy you're here"
    result = contractions.expand(text, leftovers=False, slang=False)
    assert result == "I am happy you are here"


def test_expand_invalid_input() -> None:
    with pytest.raises(TypeError, match="text must be a string"):
        contractions.expand(None)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="text must be a string"):
        contractions.expand(123)  # type: ignore[arg-type]


def test_add_invalid_input() -> None:
    with pytest.raises(TypeError, match="contraction must be a string"):
        contractions.add(123, "test")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="expansion must be a string"):
        contractions.add("test", 456)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="contraction cannot be empty"):
        contractions.add("", "test")
    with pytest.raises(ValueError, match="expansion cannot be empty"):
        contractions.add("test", "")


def test_add_dict_invalid_input() -> None:
    with pytest.raises(TypeError, match="contractions_dict must be a dict"):
        contractions.add_dict("not a dict")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="contractions_dict must be a dict"):
        contractions.add_dict(123)  # type: ignore[arg-type]


def test_fix_deprecated_alias() -> None:
    with pytest.warns(DeprecationWarning, match="fix\\(\\) is deprecated.*Use expand\\(\\) instead"):
        result = contractions.fix("you're happy")
    assert result == "you are happy"


def test_shortcuts() -> None:
    assert contractions.e("you're") == "you are"
    preview_result = contractions.p("it's", 5)
    assert len(preview_result) == 1
    assert preview_result[0]["match"] == "it's"
