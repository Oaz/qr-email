# Use an official Ubuntu runtime as a parent image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    unzip \
    git \
    wget \
    openjdk-8-jdk \
    build-essential \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-venv \
    cmake \
    ninja-build \
    clang \
    gtk+-3.0 \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libgif-dev \
    libfreetype6-dev \
    zlib1g-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libraqm-dev \
    libxcb1-dev \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    liblcms2-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libimagequant-dev \
    libx11-dev \
    libjbig-dev \
    libheif-dev \
    libraw-dev \
    libxml2-dev \
    libxslt-dev \
    libqpdf-dev \
    && apt-get clean

# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install Flutter
RUN git clone https://github.com/flutter/flutter.git -b stable /flutter
ENV PATH="/flutter/bin:/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Run flutter doctor to ensure everything is set up correctly
RUN flutter doctor

# Install Flet
RUN pip install flet

# Install Pillow
RUN pip install --no-cache-dir --only-binary :all: pikepdf
RUN pip install --no-cache-dir --only-binary :all: Pillow
RUN pip install --no-cache-dir --only-binary :all: lxml

RUN pip install --no-cache-dir --only-binary :all: img2pdf


# Set the working directory
WORKDIR /app

# Use ENTRYPOINT to set a default command and CMD to provide default arguments
ENTRYPOINT ["flet"]
CMD ["--help"]
