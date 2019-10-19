# Download git repo
FROM alpine:latest AS clone-repo-stage

ARG GIT_BRANCH
ARG IS_LOCAL
ENV PATH_CLONE /opt/hose-sound
RUN apk update && apk add git
RUN git clone --depth 1 -b ${GIT_BRANCH} https://github.com/Gnonpi/hose-sound ${PATH_CLONE}

RUN if [ ${IS_LOCAL} == "1" ]; then rm -rf ${PATH_CLONE} && mv /tmp/hose-local-repo ${PATH_CLONE}; fi
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
    yarn add semver
# npm apparently doesn't bring semver
RUN cd ${FRONT_HOSE_DIR} && \
    yarn run build


# Build back-end
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

ENV HOSE_DIR /opt/hose-sound
ENV FRONT_HOSE_DIR /opt/front_hose/
ENV STORE_STATIC_DIR /opt/

COPY --from=clone-repo-stage ${HOSE_DIR} ${HOSE_DIR}
RUN rm -rf ${HOSE_DIR}/hose/front_hose

 RUN apk update && apk add postgresql-dev gcc musl-dev
RUN cd ${HOSE_DIR} && \
    pip install --upgrade pip && \
    pip install --upgrade poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-dev

RUN mkdir -p ./hose/templates && mkdir -p ./hose/static
COPY --from=front-stage ${STORE_STATIC_DIR}/templates ./hose/templates
COPY --from=front-stage ${STORE_STATIC_DIR}/static ./hose/static
COPY .env ${HOSE_DIR}/hose/.env

EXPOSE 8000
COPY entrypoint.sh /opt/bin/entrypoint.sh
RUN chmod a+x /opt/bin/entrypoint.sh
CMD ["sh", "/opt/bin/entrypoint.sh"]
