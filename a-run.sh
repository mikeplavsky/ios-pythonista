./build.sh

if [ -z $1 ]; then
    echo "Jira account is needed."
    exit 1
fi

JIRA_USER=$1
JIRA_PWD=$(security find-generic-password -a $JIRA_USER -s jira -w)

docker rm -f jira-proxy 
docker run -d -ti \
    --name jira-proxy \
    -e FLASK_DEBUG=true \
    -e JIRA_USER=$JIRA_USER \
    -e JIRA_PWD=$JIRA_PWD \
    -e JIRA_PRODUCTS="RMADFE,RMAZ,QMMP,IN,AIRGAP" \
    -p 8000:8000 \
    jira-proxy  
