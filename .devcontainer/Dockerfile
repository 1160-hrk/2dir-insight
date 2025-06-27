FROM mcr.microsoft.com/devcontainers/python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Development tools
    git \
    curl \
    wget \
    vim \
    nano \
    # Build tools
    build-essential \
    gcc \
    g++ \
    gfortran \
    make \
    cmake \
    # Scientific computing libraries
    libfftw3-dev \
    liblapack-dev \
    libblas-dev \
    pkg-config \
    # GUI and X11 libraries for PyQt6
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    libglew-dev \
    libglfw3-dev \
    libgles2-mesa-dev \
    libegl1-mesa-dev \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    # Qt6 development tools and libraries
    qt6-base-dev \
    qt6-tools-dev \
    qt6-tools-dev-tools \
    qmake6 \
    libqt6core6 \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6opengl6-dev \
    # Additional Qt6 development packages
    qt6-base-private-dev \
    libqt6core5compat6-dev \
    # Python Qt6 system packages as fallback
    python3-pyqt6 \
    # X11 and display
    x11-apps \
    x11-utils \
    x11-xserver-utils \
    xvfb \
    # Fonts
    fonts-dejavu-core \
    fontconfig \
    # Additional utilities
    tree \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Set Qt6 environment variables
ENV QT_SELECT=6
ENV QT_QPA_PLATFORM=offscreen
ENV QMAKE=/usr/bin/qmake6

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Install PyQt6 with proper configuration
# First try with pip, if that fails use system package
RUN pip install --no-cache-dir sip PyQt6-sip && \
    (pip install --no-cache-dir PyQt6>=6.5.0 || \
    echo "Using system PyQt6 package" && \
    python3 -c "import PyQt6; print('PyQt6 system package verified')")

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . .

# Create directories for data and notebooks
RUN mkdir -p /workspace/data/sample_spectra/{cosy,tocsy,noesy} \
    && mkdir -p /workspace/notebooks/{tutorials,examples,playground}

# Set Python path
ENV PYTHONPATH=/workspace/src:$PYTHONPATH

# Configure git (will be overridden by user's git config)
RUN git config --global --add safe.directory /workspace

# Set up shell environment
RUN echo 'alias ll="ls -la"' >> /home/vscode/.bashrc && \
    echo 'alias la="ls -la"' >> /home/vscode/.bashrc && \
    echo 'export PYTHONPATH="/workspace/src:$PYTHONPATH"' >> /home/vscode/.bashrc && \
    echo 'export QT_X11_NO_MITSHM=1' >> /home/vscode/.bashrc && \
    echo 'export QT_GRAPHICSSYSTEM="native"' >> /home/vscode/.bashrc

# Create GUI testing script
RUN echo '#!/usr/bin/env python3' > /usr/local/bin/test-gui.py && \
    echo 'import sys' >> /usr/local/bin/test-gui.py && \
    echo 'try:' >> /usr/local/bin/test-gui.py && \
    echo '    from PyQt6.QtWidgets import QApplication, QLabel, QWidget' >> /usr/local/bin/test-gui.py && \
    echo '    from PyQt6.QtCore import Qt' >> /usr/local/bin/test-gui.py && \
    echo '    app = QApplication(sys.argv)' >> /usr/local/bin/test-gui.py && \
    echo '    window = QWidget()' >> /usr/local/bin/test-gui.py && \
    echo '    window.setWindowTitle("GUI Test - 2dir-insight")' >> /usr/local/bin/test-gui.py && \
    echo '    window.setGeometry(100, 100, 400, 200)' >> /usr/local/bin/test-gui.py && \
    echo '    label = QLabel("GUI動作確認成功！\\n2dir-insightのGUIが利用可能です", window)' >> /usr/local/bin/test-gui.py && \
    echo '    label.setAlignment(Qt.AlignmentFlag.AlignCenter)' >> /usr/local/bin/test-gui.py && \
    echo '    label.setGeometry(50, 50, 300, 100)' >> /usr/local/bin/test-gui.py && \
    echo '    window.show()' >> /usr/local/bin/test-gui.py && \
    echo '    print("GUI window displayed successfully!")' >> /usr/local/bin/test-gui.py && \
    echo '    print("Close the window to continue...")' >> /usr/local/bin/test-gui.py && \
    echo '    sys.exit(app.exec())' >> /usr/local/bin/test-gui.py && \
    echo 'except Exception as e:' >> /usr/local/bin/test-gui.py && \
    echo '    print(f"GUI test failed: {e}")' >> /usr/local/bin/test-gui.py && \
    echo '    sys.exit(1)' >> /usr/local/bin/test-gui.py && \
    chmod +x /usr/local/bin/test-gui.py 