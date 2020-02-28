"""Test merger of user configurations."""
import yaml
from pytest import raises
from cvcreator import merge


def test_merge_single(person1):
    """Behavior check when a single element is passed to merge."""
    merged = merge.merge_configurations([person1])
    assert merged["Summary"] == [person1["Summary"]]
    assert merged["Skills"] == person1["Skills"]
    assert merged["Languages"]["Norwegian"] == [person1["Languages"]["Norwegian"]]
    assert merged["Basic"]["Name"] == [person1["Basic"]["Name"]]


def test_merge_multiple(person1, person2):
    """Behavior check when multiple elements are passed to merge."""
    merged = merge.merge_configurations([person1, person2])
    assert merged["Basic"]["Name"] == ["Kari Brunost", "Ola Norman"]
    assert merged["Skills"]["Scientific"] == ["Mathematical Modelling"]
    assert merged["Skills"]["Frameworks"] == ["GIS", "Keras/Tensorflow", "NumPy/SciPy", "Pandas"]
    assert merged["Skills"]["Tools"] == ["Docker", "Excel", "Git", "Linux", "Matlab"]
    assert merged["Languages"]["Norwegian"] == ["Mother tongue", "Native"]
    assert merged["Languages"]["German"] == ["Basic"]
    assert merged["Projects"][0]["Activity"] == "Drug dealing"
    assert merged["Projects"][1]["Activity"] == "Selling the crown jewels"


def test_merge_illigal_value():
    """Behavior check when illigal elements are passed to merge."""
    with raises(ValueError):
        merged = merge.merge_configurations([object()])
