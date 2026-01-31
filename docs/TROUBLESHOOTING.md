# Troubleshooting Guide

This guide helps you solve common problems with the Micro-Country of Geniuses system.

## Table of Contents

1. [Installation Problems](#installation-problems)
2. [Startup Problems](#startup-problems)
3. [Runtime Problems](#runtime-problems)
4. [Performance Problems](#performance-problems)
5. [Database Problems](#database-problems)
6. [Ministry-Specific Problems](#ministry-specific-problems)
7. [Getting Help](#getting-help)

---

## Installation Problems

### Python Not Found

**Symptom**:
```
'python' is not recognized as an internal or external command
```

**Cause**: Python is not installed or not in your system PATH.

**Solution**:

1. **Check if Python is installed**:
   - Windows: Open Command Prompt, type `python --version`
   - macOS/Linux: Open Terminal, type `python3 --version`

2. **If not installed**: Follow [Installation Guide](INSTALLATION.md#step-1-install-python)

3. **If installed but not found** (Windows):
   - Reinstall Python
   - During installation, check "Add Python to PATH"
   - Restart Command Prompt

4. **If installed but not found** (macOS/Linux):
   - Use `python3` instead of `python`
   - Or create an alias: `alias python=python3`

---

### pip Not Found

**Symptom**:
```
'pip' is not recognized as an internal or external command
```

**Solution**:
```bash
# Use Python's module syntax
python -m pip install -r requirements.txt

# Or on macOS/Linux
python3 -m pip install -r requirements.txt
```

---

### Virtual Environment Won't Activate

**Symptom** (Windows):
```
venv\Scripts\activate : File cannot be loaded because running scripts is disabled
```

**Cause**: PowerShell execution policy blocks scripts.

**Solution**:
```powershell
# Option 1: Use Command Prompt instead of PowerShell
cmd
venv\Scripts\activate

# Option 2: Change PowerShell policy (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Symptom** (macOS/Linux):
```
source: command not found
```

**Cause**: Using wrong shell.

**Solution**:
```bash
# Use bash explicitly
bash
source venv/bin/activate
```

---

### Module Not Found During pip Install

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement mcp>=1.0.0
```

**Cause**: Package doesn't exist or pip index is outdated.

**Solution**:
```bash
# Update pip
python -m pip install --upgrade pip

# Update package index
python -m pip install --upgrade pip setuptools wheel

# Try installing again
pip install -r requirements.txt
```

---

### Permission Denied

**Symptom** (Linux/macOS):
```
Permission denied: '/usr/local/lib/python3.x/...'
```

**Cause**: Trying to install globally without permissions.

**Solution**:
```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: Install for current user only
pip install --user -r requirements.txt
```

---

## Startup Problems

### Ollama Not Running

**Symptom**:
```
Could not connect to Ollama at http://localhost:11434
Connection refused
```

**Cause**: Ollama server is not running.

**Solution**:

1. **Start Ollama in a separate terminal**:
   ```bash
   ollama serve
   ```

2. **Keep that terminal open** while using the system

3. **Verify it's running**:
   ```bash
   curl http://localhost:11434/api/tags
   ```
   You should see a JSON response with available models.

---

### Model Not Found

**Symptom**:
```
Model 'mistral:7b' not found
```

**Cause**: The AI model hasn't been downloaded.

**Solution**:
```bash
# Download the model (may take 5-15 minutes)
ollama pull mistral:7b

# Verify it's available
ollama list
```

---

### Wrong Model Specified

**Symptom**:
```
Model 'my-custom-model' not found
```

**Cause**: config.yaml references a model you don't have.

**Solution**:

1. **See available models**:
   ```bash
   ollama list
   ```

2. **Edit config.yaml** to use an available model:
   ```yaml
   ollama:
     model: "mistral:7b"  # Use a model from the list
   ```

---

### Database Initialization Failed

**Symptom**:
```
sqlite3.OperationalError: unable to open database file
```

**Cause**: The `data/` directory doesn't exist or no write permission.

**Solution**:
```bash
# Create the data directory
mkdir -p data

# On Linux/macOS, ensure write permission
chmod 755 data
```

---

### Port Already in Use

**Symptom**:
```
Address already in use: localhost:11434
```

**Cause**: Another Ollama instance is running.

**Solution**:

**Windows**:
```cmd
# Find the process
netstat -ano | findstr :11434

# Kill it (replace PID with the number from above)
taskkill /PID <PID> /F
```

**macOS/Linux**:
```bash
# Find and kill the process
lsof -i :11434
kill -9 <PID>
```

---

## Runtime Problems

### Requests Hang Forever

**Symptom**: You type a request and nothing happens for a very long time.

**Possible Causes and Solutions**:

1. **Model is too large for your RAM**:
   - Use a smaller model:
     ```bash
     ollama pull qwen2.5:7b
     ```
   - Edit config.yaml:
     ```yaml
     ollama:
       model: "qwen2.5:7b"
     ```

2. **Ollama crashed silently**:
   - Check the Ollama terminal for errors
   - Restart Ollama: `ollama serve`

3. **Request is too complex**:
   - Break into smaller requests
   - Be more specific

**Workaround**: Press `Ctrl+C` to cancel the current request.

---

### Garbled or Incomplete Responses

**Symptom**: Response cuts off mid-sentence or contains strange characters.

**Cause**: Context length exceeded or model issues.

**Solution**:

1. **Simplify your request**:
   - Remove unnecessary context
   - Ask one thing at a time

2. **Increase context length** in config.yaml:
   ```yaml
   ollama:
     options:
       num_ctx: 8192
   ```

3. **Restart the system** to clear context.

---

### "Ministry Not Found" Error

**Symptom**:
```
Unknown ministry: xyz
```

**Cause**: Typo in ministry name or using /ministry command incorrectly.

**Valid ministry names**:
- `code`
- `research`
- `quality`
- `operations`
- `archives`
- `communications`

**Correct usage**:
```
> /ministry code Design a REST API
> /ministry quality Run security audit
```

---

### Debate Takes Too Long / Timeout

**Symptom**: `/debate` command times out or runs for a very long time.

**Cause**: Debates involve multiple sequential LLM calls. With slow models, this compounds.

**Expected timing** (with GPU-accelerated model):
- Simple request: 5-15 seconds
- Debate (2 participants, 1 round): 30-60 seconds
- Debate (3 participants, 3 rounds): 3-5 minutes

**Solutions**:

1. **Use a faster model** that fits in GPU (see GPU/VRAM section above)

2. **Watch for progress** - the system now shows progress like:
   ```
   [Round 1/1] Gathering initial positions...
     [1/3] architect is thinking...
     [1/3] architect done.
   ```

3. **Increase timeout** in config.yaml if needed:
   ```yaml
   ollama:
     timeout: 300  # 5 minutes
   ```

4. Press `Ctrl+C` to cancel if stuck

---

### JSON Parsing Errors

**Symptom**:
```
json.decoder.JSONDecodeError: Expecting value
```

**Cause**: Model returned invalid JSON.

**Solution**:
1. **Retry the request** - Sometimes models have off moments
2. **Simplify the request** - Complex requests may confuse the model
3. **Check Ollama logs** - The model may have errored

---

## Performance Problems

### GPU/VRAM Requirements (IMPORTANT)

**The model must fit in your GPU's VRAM for fast inference.**

| GPU VRAM | Recommended Model | Size |
|----------|-------------------|------|
| 4 GB | mistral:7b, llama3.2 | 2-4 GB |
| 6-8 GB | qwen2.5:7b, deepseek-r1:7b | 4-5 GB |
| 12+ GB | qwen2.5:14b, larger models | 8-14 GB |

**Check your GPU VRAM**:
```bash
# Windows/Linux with NVIDIA
nvidia-smi

# Look for "Memory-Usage" column
```

**If model is larger than VRAM**:
- Model runs partially on CPU = VERY SLOW (4-5 tokens/sec)
- Use a smaller model that fits entirely in VRAM

**Example**: RTX 3050 (4GB VRAM) cannot run a 13GB model efficiently.

---

### Other Applications Using GPU

**Symptom**: Slow responses even with adequate GPU.

**Cause**: Other apps (LM Studio, games, video editors) using GPU memory.

**Solution**:
```bash
# Check what's using GPU (Windows/Linux)
nvidia-smi

# Close other GPU-intensive applications
# Especially: LM Studio, CUDA applications, games
```

---

### Very Slow Responses

**Possible Causes and Solutions**:

| Cause | Solution |
|-------|----------|
| Model too large for GPU | Use smaller model (mistral:7b) |
| Other apps using GPU | Close LM Studio, games, etc. |
| Insufficient RAM | Close other applications |
| No GPU acceleration | Install CUDA drivers |
| Complex request | Break into smaller parts |

**Quick diagnosis**:
```bash
# Test model speed directly
ollama run mistral:7b "Say hello" --verbose

# Look for "eval rate" - should be 15+ tokens/sec with GPU
# If under 5 tokens/sec, model is running on CPU
```

**Check system resources**:

**Windows**: Task Manager (Ctrl+Shift+Esc) → Performance tab

**macOS**: Activity Monitor → Memory/CPU

**Linux**: `htop` or `top`

---

### High Memory Usage

**Symptom**: System becomes sluggish, swap usage increases.

**Solution**:

1. **Use a smaller model**:
   ```bash
   ollama pull qwen2.5:7b
   ```

2. **Reduce context size** in config.yaml:
   ```yaml
   ollama:
     options:
       num_ctx: 4096  # Reduce from 8192
   ```

3. **Restart between long sessions** to clear memory.

---

### GPU Not Being Used

**Symptom**: Responses are slow even with a capable GPU.

**Check if GPU is detected**:
```bash
ollama run mistral:7b
# Type: /show info
# Look for GPU information
```

**Solution** (NVIDIA):
1. Install CUDA drivers
2. Restart Ollama
3. Verify with `nvidia-smi`

---

## Database Problems

### Database Locked

**Symptom**:
```
sqlite3.OperationalError: database is locked
```

**Cause**: Multiple processes accessing the database.

**Solution**:
1. **Close all instances** of the system
2. **Remove lock file** (if exists):
   ```bash
   rm data/country.db-journal
   rm data/country.db-wal
   ```
3. **Restart the system**

---

### Corrupted Database

**Symptom**:
```
sqlite3.DatabaseError: database disk image is malformed
```

**Cause**: Incomplete write, crash, or disk error.

**Solution**:

1. **Try to recover**:
   ```bash
   sqlite3 data/country.db ".recover" | sqlite3 data/country_recovered.db
   mv data/country.db data/country_backup.db
   mv data/country_recovered.db data/country.db
   ```

2. **If recovery fails**, start fresh:
   ```bash
   rm data/country.db
   # Database will be recreated on next run
   ```

---

### Data Not Persisting

**Symptom**: Stored decisions and knowledge disappear after restart.

**Possible Causes**:

1. **Wrong database path**:
   - Check config.yaml points to correct path
   - Ensure path exists

2. **Running from different directory**:
   - Always run from the `micro-country` folder
   - Database path is relative to working directory

3. **Permissions issue**:
   ```bash
   chmod 644 data/country.db
   ```

---

## Ministry-Specific Problems

### Code Ministry

**"Code generation incomplete"**
- Request was too complex
- Break into smaller functions
- Provide more specific requirements

**"Syntax error in generated code"**
- Model made a mistake
- Request review or regeneration
- Manually fix small errors

---

### Quality Ministry

**"Tests fail to run"**
- Check pytest is installed: `pip install pytest`
- Verify test file paths are correct
- Check for import errors in test files

**"Security audit too vague"**
- Provide specific code to audit
- Mention focus areas (auth, input validation, etc.)

---

### Operations Ministry

**"Permission denied" for file operations**
- Check file/folder permissions
- Run with appropriate privileges
- Verify paths are correct

**"Command execution failed"**
- Command may not exist on your system
- Check spelling
- Verify command is in PATH

---

### Archives Ministry

**"Cannot recall decision"**
- Decision may not have been stored
- Check spelling of topic
- Try broader search terms

---

## Getting Help

### Collecting Debug Information

When seeking help, gather this information:

1. **System info**:
   ```bash
   python --version
   ollama --version
   ```

2. **Error message**: Copy the complete error

3. **Steps to reproduce**: What did you do before the error?

4. **Config**: Share your config.yaml (remove sensitive info)

5. **Logs**: Check Ollama terminal for errors

### Self-Diagnosis Checklist

Before asking for help, verify:

- [ ] Ollama is running (`ollama serve`)
- [ ] Model is downloaded (`ollama list`)
- [ ] Virtual environment is active (`(venv)` in prompt)
- [ ] Dependencies are installed (`pip list`)
- [ ] Running from correct directory (`ls` shows orchestrator.py)
- [ ] Config.yaml has correct model name

### Reset to Known Good State

If all else fails:

```bash
# Stop all processes
# Windows: Close all terminals
# Linux/macOS: pkill -f python; pkill -f ollama

# Remove database (loses all data!)
rm data/country.db

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Restart Ollama
ollama serve

# In new terminal, start system
python orchestrator.py
```

---

## Error Message Reference

| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| `Connection refused` | Ollama not running | `ollama serve` |
| `Model not found` | Model not downloaded | `ollama pull mistral:7b` |
| `Module not found` | Dependencies missing | `pip install -r requirements.txt` |
| `Permission denied` | File permissions | Check permissions, use venv |
| `Database locked` | Multiple instances | Close other instances |
| `Out of memory` | Model too large | Use smaller model |
| `Timeout` | Request too complex | Simplify request |
| `JSON decode error` | Model output issue | Retry request |

---

## Still Stuck?

1. **Re-read the relevant documentation** section
2. **Try the exact commands** from the guides (don't modify them)
3. **Start fresh** with a new terminal/command prompt
4. **Check for typos** in commands and file names
5. **Restart your computer** (clears all stuck processes)

Most problems are solved by ensuring:
1. Ollama is running
2. Model is downloaded
3. Virtual environment is active
4. You're in the correct directory
