import glob
import os

from pytest import fixture

from cvcreator.vitae.tech_skills import get_skills_data

CURDIR = os.path.dirname(os.path.abspath(__file__))
CODEDIR = os.path.abspath(os.path.join(os.path.pardir, "cvcreator"))


@fixture
def skills_data():
    return get_skills_data()


def test_icon_reference(skills_data):
    for iconpath in glob.glob(os.path.join(CODEDIR, "icons", "*.pdf")):
        assert os.path.splitext(os.path.basename(iconpath))[0] in skills_data["skills"].keys(), (
            f"Icon {iconpath} does not have a tech skill counterpart.")


def test_skills_labels(skills_data):
    unknown_labels = {
        label for labels in skills_data["skills"].values()
        for label in labels
    }.difference(skills_data["allowed_labels"])
    assert not unknown_labels, f"Label not recognized: {unknown_labels}"


def test_short_maps(skills_data):
    unknown_keys = set(skills_data["short_map"]).difference(skills_data["skills"])
    assert not unknown_keys, f"Shortmap key not recognized: {unknown_keys}"
    unknown_vals = set(skills_data["short_map"].values()).difference(skills_data["skills"])
    assert not unknown_vals, f"Shortmap value not recognized: {unknown_vals}"

