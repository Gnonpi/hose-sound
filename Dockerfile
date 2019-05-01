# Build front-end
FROM node:11-alpine AS front-stage

ENV front_hose_dir ./hose/front_hose
ENV store_static_dir /tmp/front_hose-built
WORKDIR /app

COPY ${front_hose_dir}/package*.json ./
COPY ${front_hose_dir}/yarn.lock ./
RUN yarn install --prod

COPY ${front_hose_dir}/ .

RUN mkdir -p ./hose/templates && mkdir -p ./hose/static
RUN yarn run build
RUN mkdir -p ${store_static_dir}/templates && \
    mkdir -p ${store_static_dir}/static && \
    cp -R ./hose/templates ${store_static_dir}/templates && \
    cp -R ./hose/static ${store_static_dir}/static

RUN ls ${store_static_dir}/templates && \
    ls ${store_static_dir}/static

# Build back-end
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
ENV store_static_dir /tmp/front_hose-built

RUN mkdir /code
WORKDIR /code

COPY pyproject.toml poetry.lock ${WORK_DIR}/
RUN apk update && apk add libc-dev gcc postgresql-dev
RUN pip install --upgrade pip && \
    pip install --upgrade poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev && \
    pip uninstall -y poetry

COPY ./hose/hose ./hose/hose
COPY ./hose/hose_usage ./hose/hose_usage
COPY ./hose/.env ./hose/manage.py ./hose/

RUN mkdir -p ./hose/templates && mkdir -p ./hose/static
COPY --from=front-stage ${store_static_dir}/templates ./hose/templates
COPY --from=front-stage ${store_static_dir}/static ./hose/static

EXPOSE 8000
CMD ["python3", "hose/manage.py", "runserver"]
