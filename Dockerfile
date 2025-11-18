FROM continuumio/miniconda3

# Create environment + install torch + clean
RUN conda create -n chatterbox python=3.11 -y && \
    \
    /opt/conda/envs/chatterbox/bin/pip install \
        torch==2.9.1+cu128 \
        torchaudio==2.9.1+cu128 \
        --index-url https://download.pytorch.org/whl/cu128 \
    && \
    conda clean -a -y && \
    rm -rf /opt/conda/pkgs && \
    rm -rf /root/.cache/pip && \
    rm -rf /tmp/* && \
    find /opt/conda/envs/chatterbox -name "*.pyc" -delete && \
    find /opt/conda/envs/chatterbox -name "__pycache__" -type d -exec rm -rf {} +

# Make env active
ENV PATH="/opt/conda/envs/chatterbox/bin:$PATH"

# App settings
ENV GRADIO_TEMP_DIR="/app/output"
ENV GRADIO_SERVER_NAME="0.0.0.0"


# Project dependecies
COPY pyproject.toml .
COPY src ./src

# Install project and clean cache
RUN pip install . && \
    rm -rf /root/.cache/pip && \
    rm -rf /tmp/*

# Copy rest of the project
WORKDIR /app
COPY . .

# Start gradio
CMD ["python", "multilingual_app.py"]