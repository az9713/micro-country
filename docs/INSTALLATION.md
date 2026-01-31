# Installation Guide

This guide walks you through every step of installing the Micro-Country of Geniuses system. No prior experience with Python or AI systems is required.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Step 1: Install Python](#step-1-install-python)
3. [Step 2: Install Ollama](#step-2-install-ollama)
4. [Step 3: Download AI Model](#step-3-download-ai-model)
5. [Step 4: Set Up the Project](#step-4-set-up-the-project)
6. [Step 5: Install Dependencies](#step-5-install-dependencies)
7. [Step 6: Initialize Database](#step-6-initialize-database)
8. [Step 7: Verify Installation](#step-7-verify-installation)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

Before starting, verify your computer meets these requirements:

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 16 GB | 32 GB |
| Disk Space | 20 GB free | 50 GB free |
| CPU | 4 cores | 8+ cores |
| GPU | Not required | NVIDIA GPU (faster) |

### Operating System

- **Windows**: Windows 10 version 1903 or later, Windows 11
- **macOS**: macOS 10.15 (Catalina) or later
- **Linux**: Ubuntu 20.04+, Debian 11+, Fedora 35+

### How to Check Your System

**Windows**:
1. Press `Windows + R`
2. Type `msinfo32` and press Enter
3. Look for "Installed Physical Memory (RAM)" and "Processor"

**macOS**:
1. Click the Apple menu () → "About This Mac"
2. See Memory and Processor information

**Linux**:
```bash
# Check RAM
free -h

# Check CPU
lscpu

# Check disk space
df -h
```

---

## Step 1: Install Python

### What is Python?

Python is a programming language. This project is written in Python, so you need it installed to run the system.

### Windows Installation

1. **Download Python**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click the yellow "Download Python 3.12.x" button
   - A file like `python-3.12.x-amd64.exe` will download

2. **Run the Installer**
   - Double-click the downloaded file
   - **IMPORTANT**: Check the box that says "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**
   - Press `Windows + R`
   - Type `cmd` and press Enter
   - In the black window, type:
     ```
     python --version
     ```
   - You should see something like: `Python 3.12.1`

### macOS Installation

1. **Download Python**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Click "Download Python 3.12.x"
   - A `.pkg` file will download

2. **Run the Installer**
   - Double-click the downloaded file
   - Follow the installation wizard
   - Click "Continue" through the screens
   - Click "Install"
   - Enter your password when prompted

3. **Verify Installation**
   - Open Terminal (Applications → Utilities → Terminal)
   - Type:
     ```bash
     python3 --version
     ```
   - You should see: `Python 3.12.1`

### Linux Installation

Most Linux distributions come with Python. If not:

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora**:
```bash
sudo dnf install python3 python3-pip
```

**Verify**:
```bash
python3 --version
```

---

## Step 2: Install Ollama

### What is Ollama?

Ollama is a program that runs AI models on your computer. It's like having a small ChatGPT running locally on your machine.

### Windows Installation

1. **Download Ollama**
   - Go to [ollama.ai/download](https://ollama.ai/download)
   - Click "Download for Windows"
   - A file like `OllamaSetup.exe` will download

2. **Run the Installer**
   - Double-click the downloaded file
   - If Windows asks "Do you want to allow this app?", click "Yes"
   - Follow the installation wizard
   - Click "Install"

3. **Verify Installation**
   - Open Command Prompt (Windows + R, type `cmd`, Enter)
   - Type:
     ```
     ollama --version
     ```
   - You should see a version number

### macOS Installation

1. **Download Ollama**
   - Go to [ollama.ai/download](https://ollama.ai/download)
   - Click "Download for macOS"
   - A `.zip` file will download

2. **Install**
   - Double-click the downloaded file to unzip
   - Drag "Ollama" to your Applications folder
   - Double-click Ollama in Applications to start it
   - You'll see an Ollama icon in your menu bar

3. **Verify Installation**
   - Open Terminal
   - Type:
     ```bash
     ollama --version
     ```

### Linux Installation

```bash
# One-command installation
curl -fsSL https://ollama.ai/install.sh | sh

# Verify
ollama --version
```

---

## Step 3: Download AI Model

### What is an AI Model?

An AI model is the "brain" that processes your requests. We'll download a model called "qwen2.5:14b" which is good at coding and reasoning.

### Start Ollama Server

**Windows**:
1. Open Command Prompt
2. Type:
   ```
   ollama serve
   ```
3. Leave this window open (don't close it!)

**macOS**:
- Ollama usually starts automatically
- Check for the Ollama icon in the menu bar
- If not running, open Terminal and type `ollama serve`

**Linux**:
```bash
ollama serve
```

### Download the Model

**Open a NEW terminal/command prompt** (keep the server running):

```bash
ollama pull qwen2.5:14b
```

This will download about 9GB. It may take 10-30 minutes depending on your internet speed.

**What you'll see**:
```
pulling manifest
pulling 8de95da68dc4... 100% ████████████████████████ 9.0 GB
pulling 62fbfd9ed093... 100% ████████████████████████ 182 B
...
success
```

### Alternative: Smaller Model (Faster but Less Capable)

If you have limited RAM or want faster responses:
```bash
ollama pull qwen2.5:7b
```

Then edit `config.yaml` to use it:
```yaml
ollama:
  model: "qwen2.5:7b"
```

---

## Step 4: Set Up the Project

### Option A: If You Have the Project Files

If you received the project as a folder or zip file:

1. **Extract if needed**
   - If it's a `.zip` file, right-click and choose "Extract All"

2. **Navigate to the folder**

   **Windows**:
   ```
   cd C:\path\to\micro-country
   ```

   **macOS/Linux**:
   ```bash
   cd /path/to/micro-country
   ```

### Option B: Clone from Repository

If the project is in a Git repository:

1. **Install Git** (if not already installed)
   - Windows: [git-scm.com/download/win](https://git-scm.com/download/win)
   - macOS: `xcode-select --install`
   - Linux: `sudo apt install git`

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd micro-country
   ```

---

## Step 5: Install Dependencies

### What are Dependencies?

Dependencies are other Python packages that this project needs to work. Think of them as ingredients for a recipe.

### Create a Virtual Environment (Recommended)

A virtual environment keeps this project's dependencies separate from other Python projects.

**Windows**:
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` at the start of your command line. This means the virtual environment is active.

### Install the Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `mcp` - Protocol for AI agents to communicate
- `ollama` - Client to talk to the AI model
- `aiosqlite` - Database for storing decisions
- `pyyaml` - Configuration file reading
- `httpx` - HTTP requests
- `pytest` - Testing framework

**What you'll see**:
```
Collecting mcp>=1.0.0
  Downloading mcp-1.0.0-py3-none-any.whl (45 kB)
Collecting ollama>=0.3.0
  ...
Successfully installed mcp-1.0.0 ollama-0.3.1 ...
```

---

## Step 6: Initialize Database

### What is the Database?

The database stores:
- The "Constitution" (rules for the AI)
- Decisions that were made
- Knowledge learned over time
- Task history

### Initialize

The database is created automatically when you first run the system. But you can initialize it manually:

```bash
python -c "
import asyncio
from shared.database import Database

async def init():
    db = Database('data/country.db')
    await db.initialize()
    print('Database initialized!')

asyncio.run(init())
"
```

You should see:
```
Database initialized!
```

---

## Step 7: Verify Installation

### Run the Tests

Tests verify everything is installed correctly:

```bash
python -m pytest tests/ -v
```

**Expected output**:
```
========================= test session starts ==========================
tests/test_genius_protocol.py::TestReasoningTrace::test_create_trace PASSED
tests/test_genius_protocol.py::TestReasoningTrace::test_complete_trace PASSED
tests/test_database.py::test_initialize_database PASSED
...
========================= X passed in Y.YYs ============================
```

All tests should pass. If some fail, see [Troubleshooting](#troubleshooting).

### Run the System

```bash
python orchestrator.py
```

**Expected output**:
```
Starting Micro-Country Orchestrator...
✓ Connected to Ollama at http://localhost:11434
✓ Model qwen2.5:14b available
...
Orchestrator ready!

============================================================
Welcome to the Micro-Country of Geniuses
============================================================
>
```

### Try a Simple Request

Type:
```
> Hello, what can you do?
```

If you get a response, congratulations! Installation is complete.

Type `/quit` to exit.

---

## Troubleshooting

### "python is not recognized"

**Problem**: Windows doesn't know where Python is.

**Solution**:
1. Reinstall Python
2. Make sure to check "Add Python to PATH"
3. Restart Command Prompt after installation

### "pip is not recognized"

**Problem**: pip (Python's package installer) is not in PATH.

**Solution**:
```bash
python -m pip install -r requirements.txt
```

### "Could not connect to Ollama"

**Problem**: Ollama server isn't running.

**Solution**:
1. Open a terminal
2. Run `ollama serve`
3. Keep that terminal open
4. Try again in a different terminal

### "Model not found"

**Problem**: The AI model isn't downloaded.

**Solution**:
```bash
ollama pull qwen2.5:14b
```

### "Out of memory"

**Problem**: Not enough RAM for the model.

**Solution**:
1. Use a smaller model:
   ```bash
   ollama pull qwen2.5:7b
   ```
2. Edit `config.yaml`:
   ```yaml
   ollama:
     model: "qwen2.5:7b"
   ```

### "Permission denied" on Linux/macOS

**Problem**: File permissions issue.

**Solution**:
```bash
chmod +x orchestrator.py
```

### Tests Fail

**Problem**: Some component isn't installed correctly.

**Solution**:
1. Make sure virtual environment is active
2. Reinstall dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Check Python version:
   ```bash
   python --version  # Should be 3.11+
   ```

### "Module not found" Errors

**Problem**: Dependencies not installed or wrong directory.

**Solution**:
1. Make sure you're in the `micro-country` folder
2. Make sure virtual environment is active (see `(venv)` in prompt)
3. Install dependencies again:
   ```bash
   pip install -r requirements.txt
   ```

---

## Next Steps

Installation complete! Now:

1. Go to the [Quick Start Guide](QUICK_START.md) for hands-on examples
2. Read the [User Guide](USER_GUIDE.md) for all features
3. Explore the [Architecture](ARCHITECTURE.md) if you're curious how it works

---

## Uninstalling

If you need to remove the system:

### Remove the Project
Delete the `micro-country` folder.

### Remove Python Dependencies
```bash
pip uninstall -r requirements.txt -y
```

### Remove Virtual Environment
Delete the `venv` folder inside `micro-country`.

### Remove Ollama
- **Windows**: Use "Add or Remove Programs"
- **macOS**: Delete Ollama from Applications
- **Linux**: `sudo rm /usr/local/bin/ollama`

### Remove AI Models
```bash
ollama rm qwen2.5:14b
```
