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

# Install project with dev dependencies using uv
RUN /root/.local/bin/uv pip install --system --break-system-packages -e ".[dev]"
