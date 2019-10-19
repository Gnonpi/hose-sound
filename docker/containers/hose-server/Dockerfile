# Download git repo
FROM alpine:latest AS clone-repo-stage

ARG GIT_BRANCH
ENV PATH_CLONE /opt/hose-sound
RUN apk update && apk add git
RUN git clone --depth 1 -b ${GIT_BRANCH} https://github.com/Gnonpi/hose-sound ${PATH_CLONE}

# Build front-end
FROM node:11-alpine AS front-stage

ENV PATH_CLONE /opt/hose-sound
ENV FRONT_HOSE_DIR /opt/front_hose/
ENV STORE_STATIC_DIR /opt/

RUN mkdir -p ${FRONT_HOSE_DIR} && \
    mkdir -p ${STORE_STATIC_DIR}

COPY --from=clone-repo-stage ${PATH_CLONE}/hose/front_hose ${FRONT_HOSE_DIR}

RUN mkdir -p ${STORE_STATIC_DIR}/templates && \
    mkdir -p ${STORE_STATIC_DIR}/static

RUN cd ${FRONT_HOSE_DIR} && \
    yarn install --prod && \
    yarn run build

RUN cp -R ./hose/templates ${STORE_STATIC_DIR}/templates && \
    cp -R ./hose/static ${STORE_STATIC_DIR}/static

RUN ls ${STORE_STATIC_DIR}/templates && \
    ls ${STORE_STATIC_DIR}/static

# Build back-end
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
ENV store_static_dir /tmp/front_hose-built

RUN mkdir /code
WORKDIR /code

COPY ../../../pyproject.toml poetry.lock ${WORK_DIR}/
# RUN apk update && apk add libc-dev gcc
RUN pip install --upgrade pip && \
    pip install --upgrade poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev && \
    pip uninstall -y poetry

COPY ../../../hose/hose ./hose/hose
COPY ../../../hose/hose_usage ./hose/hose_usage
COPY ../../../hose/.env ./hose/manage.py ./hose/

RUN mkdir -p ./hose/templates && mkdir -p ./hose/static
COPY --from=front-stage ${STORE_STATIC_DIR}/templates ./hose/templates
COPY --from=front-stage ${STORE_STATIC_DIR}/static ./hose/static

EXPOSE 8000
CMD ["python3", "hose/manage.py", "runserver"]
