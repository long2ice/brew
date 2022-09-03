FROM python:3.9 as builder
RUN mkdir -p /brew
WORKDIR /brew
COPY pyproject.toml poetry.lock /brew/
ENV POETRY_VIRTUALENVS_CREATE false
RUN pip3 install pip --upgrade && pip3 install poetry --upgrade --pre && poetry install --no-root --only main

FROM python:3.9-slim
WORKDIR /brew
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY . /brew
CMD ["uvicorn" ,"brew.app:app", "--host", "0.0.0.0"]
