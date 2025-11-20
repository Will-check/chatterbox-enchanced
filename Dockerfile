FROM continuumio/miniconda3

# Create environment + install torch + clean
RUN conda create -n chatterbox-enchanced python=3.11 -y && \
    \
    /opt/conda/envs/chatterbox-enchanced/bin/pip install \
        torch==2.9.1+cu128 \
        torchaudio==2.9.1+cu128 \
        --index-url https://download.pytorch.org/whl/cu128 \
    && \
    conda clean -a -y && \
    rm -rf /opt/conda/pkgs && \
    rm -rf /root/.cache/pip && \
    rm -rf /tmp/* && \
    find /opt/conda/envs/chatterbox-enchanced -name "*.pyc" -delete && \
    find /opt/conda/envs/chatterbox-enchanced -name "__pycache__" -type d -exec rm -rf {} +

# Make env active
ENV PATH="/opt/conda/envs/chatterbox-enchanced/bin:$PATH"

# Project dependecies
COPY pyproject.toml .
COPY src ./src

# Install project and clean cache
RUN pip install . && \
    rm -rf /root/.cache/pip && \
    rm -rf /tmp/*

# App settings
ENV GRADIO_TEMP_DIR="/app/output"
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT="7861"

# Copy rest of the project
WORKDIR /app
# COPY . .

# Start gradio
CMD ["tail", "-f", "/dev/null"]