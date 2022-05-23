import os
from pathlib import Path
import pytest
from pyutap.nta import *
from pyutap.path_analysis import *

src_dir = Path(__file__).parent
realizable_test_dir = src_dir / "testcases" / "path_realizable"
not_realizable_test_dir = src_dir / "testcases" / "path_not_realizable"


def get_xmls(test_dir):
    paths = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".xml"):
                paths.append(str(os.path.join(root, file)))
    return paths


def get_realizable():
    return get_xmls(realizable_test_dir)


def get_not_realizable():
    return get_xmls(not_realizable_test_dir)

def convert_to_path(nta):
    path = []
    init = nta.templates[0].initial_location
    for edge in nta.templates[0].edges:
        for edge in nta.templates[0].edges:
            if edge.src.uid == init:
                path.append(edge)
                break
        init = edge.dst

    return path


@pytest.mark.parametrize("test_filename", get_realizable())
def test_realizable(test_filename):
    nta = NTAHelper(test_filename, "nta")
    path = convert_to_path(nta)

    assert is_path_realizable(path)[0] == True


@pytest.mark.parametrize("test_filename", get_not_realizable())
def test_not_realizable(test_filename):
    nta = NTAHelper(test_filename, "nta")
    path = convert_to_path(nta)

    assert is_path_realizable(path)[0] == False
