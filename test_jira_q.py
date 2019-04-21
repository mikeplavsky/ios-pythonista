import jira
import pytest

@pytest.mark.parametrize("sprints, exp",[
([
    "com.atlassian.greenhopper.service.sprint.Sprint@10c8a0c4[id=10786,rapidViewId=2049,state=CLOSED,name=QMMP Sprint 44,startDate=2019-02-18T04:17:46.523-08:00,endDate=2019-03-04T04:17:00.000-08:00,completeDate=2019-03-01T07:29:41.024-08:00,sequence=10786,goal=]",
    "com.atlassian.greenhopper.service.sprint.Sprint@6e74224b[id=10920,rapidViewId=2049,state=ACTIVE,name=QMMP Sprint 45,startDate=2019-03-04T04:47:04.556-08:00,endDate=2019-03-17T05:47:00.000-07:00,completeDate=<null>,sequence=10920,goal=]"],
    '44,45'
),
([],'no sprints'),
(None,'no sprints')
])
def test_sprints(sprints,exp):
    
    sprints =     given = dict(
        fields=dict(
            customfield_12004 = sprints))

    r = jira.sprints(given)
    assert r == exp

@pytest.mark.parametrize("points, exp",[
    (10, "10 points"),
    (0, "0 points"),
    ("", "not estimated"),
    (1,"1 point")])
def test_points(points, exp):

    given = dict(
        fields=dict(
            customfield_10303 = f"{points}"))
            
    then = jira.story_points(given)
    assert then == exp

def test_get_features():

    feature = lambda ps,s: dict(
        fields=dict(
            customfield_10303 = f"{ps}" if ps else ps,
            status=dict(name=s)))

    given = dict(issues=[
        feature(10, 'Closed'),
        feature(2, 'In Progress'),
        feature(None, 'Closed'),
        feature('', 'In Progress'),
        feature(1, 'Unresolved'),
        feature(7, 'Closed'),
        feature(3, 'Rejected')])

    res = jira.get_features(given)
    assert res == (7,3,23,17)

@pytest.mark.parametrize("versions, exp",[
    ([],"no releases"),
    ([dict(name="1"), dict(name="2")],"1,2")])
def test_versions(versions, exp):

    given = dict(
        fields = dict(
            fixVersions = versions))

    then = jira.versions(given)         
    assert then == exp 