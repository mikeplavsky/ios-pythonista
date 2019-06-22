docker build -t jira-proxy .

if [ -z $1 ]; then
    echo "Jira account is needed."
    exit 1
fi

JIRA_USER=$1
JIRA_PWD=$(security find-generic-password -a $JIRA_USER -s jira -w)

docker run -ti --rm \
    -e FLASK_DEBUG=true \
    -e JIRA_USER=$JIRA_USER \
    -e JIRA_PWD=$JIRA_PWD \
    -p 8080:8080 \
    -w /jira-proxy \
    -v "$(pwd)":/jira-proxy \
    jira-proxy \
    flask run -p 8080 -h 0.0.0.0