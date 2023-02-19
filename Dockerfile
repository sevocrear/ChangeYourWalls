FROM nvcr.io/nvidia/pytorch:20.06-py3
RUN pip install -U openmim
RUN pip install --upgrade pip setuptools
RUN mim install mmcv-full
RUN git clone https://github.com/open-mmlab/mmsegmentation.git && cd mmsegmentation && pip install -v -e .
ARG DEBIAN_FRONTEND=noninteractive
ARG UID
ARG GID
ARG UNAME
# ==== add USER ====
RUN groupadd -g ${GID} -o ${UNAME}
RUN useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${UNAME}
USER ${UNAME}
WORKDIR /home/${UNAME}
