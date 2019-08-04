if [ -z $1 ]; then
    echo "version is required"
    exit 1
fi

VERSION=$1

docker build -t jira-proxy .
docker tag jira-proxy mikeplavsky/jira-proxy:${VERSION}
docker push mikeplavsky/jira-proxy:${VERSION}
