FROM python

WORKDIR /
COPY ./requirements.txt /
RUN pip install -r requirements.txt