docker build -t jira-proxy .
docker run -ti --rm \
    -e FLASK_DEBUG=true \
    -p 8080:8080 \
    -w /jira-proxy \
    -v "$(pwd)":/jira-proxy \
    jira-proxy \
    bash