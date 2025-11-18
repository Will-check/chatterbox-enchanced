FROM continuumio/miniconda3

RUN conda create -n chatterbox python=3.11 -y
RUN echo "source activate chatterbox" >> ~/.bashrc
ENV PATH="/opt/conda/envs/chatterbox/bin:$PATH"
ENV GRADIO_TEMP_DIR="/app/output"
ENV GRADIO_SERVER_NAME="0.0.0.0"
RUN pip install torch==2.9.1+cu128 torchaudio==2.9.1+cu128 \
    --index-url https://download.pytorch.org/whl/cu128


WORKDIR /app

CMD ["tail", "-f", "/dev/null"]