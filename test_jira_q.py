import jira
import pytest

@pytest.mark.parametrize("points, res",[
    (10, "10 points"),
    (0, "0 points"),
    ("", ""),
    (1,"1 point")])
def test_points(points, res):

    given = dict(
        fields=dict(
            customfield_10303 = f"{points}"))
            
    then = jira.story_points(given)
    assert then == res 