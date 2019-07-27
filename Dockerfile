FROM python:3.7.4-alpine3.9

WORKDIR /
COPY ./requirements.txt /
RUN pip install -r requirements.txt

RUN mkdir /a-jira
WORKDIR /a-jira

ADD . /a-jira
ENV FLASK_DEBUG=1

CMD /a-jira/start.sh
