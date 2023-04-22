# This Dockerfile has buildkit syntax, to allow build steps to be cached
# and speed up when rebuilding

FROM python:3.8.8-slim-buster AS base

# Build ARGs
ARG BOT_PROJECT="anfa-bot"
ARG BOT_USER=1000
ARG BOT_GROUP=1000
ARG BOT_HOME_DIR="/srv"
ARG APP_DIR="${BOT_HOME_DIR}/app"

# Export ARGs as ENV vars so they can be shared among steps
ENV BOT_PROJECT="${BOT_PROJECT}" \
    BOT_USER="${BOT_USER}" \
    BOT_GROUP="${BOT_GROUP}" \
    BOT_HOME_DIR="${BOT_HOME_DIR}" \
    APP_DIR="${APP_DIR}" \
    DEBIAN_FRONTEND=noninteractive \
    APT_OPTS="-q=2 --no-install-recommends --yes"

RUN groupadd --gid $BOT_GROUP $BOT_PROJECT \
    && useradd --uid $BOT_USER --gid $BOT_GROUP -m $BOT_PROJECT

# Prepare a directory to run with an unprivileged user
RUN chown -cR "$BOT_PROJECT":"$BOT_PROJECT" ${BOT_HOME_DIR} && \
    usermod -d ${BOT_HOME_DIR} ${BOT_PROJECT}

################################################################################

FROM base AS builder

# Build the code as unprivileged user
USER ${BOT_PROJECT}
WORKDIR ${BOT_HOME_DIR}

COPY --chown=${BOT_PROJECT}:${BOT_PROJECT} src/ ${APP_DIR}

RUN ls ${APP_DIR}
RUN python3 -m pip install --user --requirement ${APP_DIR}/requirements.txt
RUN cd ${APP_DIR} && \
    chown -cR ${BOT_PROJECT}:${BOT_PROJECT} ${BOT_HOME_DIR} && \
    rm -rf ${BOT_HOME_DIR}/.cache && \
    find ${APP_DIR} -iname '.git*' -print0 | xargs -0 -r -t rm -rf

################################################################################

FROM base AS app

# Address the pip warning regarding PATH
ENV PATH="${PATH}:${BOT_HOME_DIR}/.local/bin"

# Import built code from previous step
COPY --from=builder ${BOT_HOME_DIR} ${BOT_HOME_DIR}

# Adjust privileges
RUN chown -R "${BOT_PROJECT}:${BOT_PROJECT}" ${BOT_HOME_DIR} && \
    usermod -d ${BOT_HOME_DIR} ${BOT_PROJECT}

# Set up to run as an unprivileged user
USER ${BOT_PROJECT}
WORKDIR ${APP_DIR}
CMD ["./entrypoint.sh"]
