FROM python:3.8.2

RUN pip install -U pip

COPY ./ .

RUN pip install -U pip && pip install --no-cache-dir pipenv

RUN pipenv install --system --deploy
RUN python setup.py install

RUN rm -rf ./dist
RUN rm -rf ./build
RUN rm -rf ./*.egg-info


ENTRYPOINT ["flake8"]

CMD ["./source_code/tests"]