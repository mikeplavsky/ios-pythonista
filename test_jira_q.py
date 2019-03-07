import jira
import pytest

@pytest.mark.parametrize("points, exp",[
    (10, "10 points"),
    (0, "0 points"),
    ("", ""),
    (1,"1 point")])
def test_points(points, exp):

    given = dict(
        fields=dict(
            customfield_10303 = f"{points}"))
            
    then = jira.story_points(given)
    assert then == exp

@pytest.mark.parametrize("versions, exp",[
    ([],"no releases"),
    ([dict(name="1"), dict(name="2")],"1,2")])
def test_versions(versions, exp):

    given = dict(
        fields = dict(
            fixVersions = versions))

    then = jira.versions(given)         
    assert then == exp 