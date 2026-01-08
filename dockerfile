# Start with a minimal TeX Live image as base and install other
# necessary packages separately to keep the image size small.
FROM texlive/texlive:latest-small

# Install additional TeX Live collections for language support
RUN tlmgr update --self && \
    tlmgr install collection-langeuropean

# Install Python and curl for uv installation
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv (Because it is the best --- Fight me!)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.rst ./
COPY cvcreator ./cvcreator

# Create virtual environment and install project with dev dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install -e ".[dev]"

# Set the entrypoint to the cv command
ENTRYPOINT ["cv"]

