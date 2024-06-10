FROM mambaorg/micromamba:latest

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

# install necessary opencv dependencies
USER root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install\
    libgl1\
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    libglib2.0-0 -y && \
    rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# copy the rest of the code
COPY . /app
WORKDIR /app

# change the owner of the file
USER root
RUN chown $MAMBA_USER:$MAMBA_USER /app/run_server.sh

# run the app
USER $MAMBA_USER
RUN chmod +x /app/run_server.sh
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "/app/run_server.sh"]