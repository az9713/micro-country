# Micro-Country of Geniuses

A **100% local** multi-agent AI system that operates like a small country of experts working together to solve complex problems. Runs entirely on your machine using [Ollama](https://ollama.ai) - no cloud APIs, no data sent externally, no API costs.

## What Is This?

Imagine having a team of AI experts at your disposal:
- An **Architect** who designs software systems
- A **Coder** who writes clean, working code
- A **Debugger** who finds and fixes bugs
- A **Tester** who ensures quality
- A **Security Auditor** who finds vulnerabilities
- And many more specialists...

This project creates that team using a local AI model (Ollama) and organizes them into "ministries" that work together.

## Why Local Models?

```
┌─────────────────────────────────────────────────────────────────┐
│                    100% LOCAL OPERATION                         │
│                                                                 │
│   Your Computer                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                         │  │
│   │   micro-country  ◄──────►  Ollama  ◄──────►  AI Model  │  │
│   │   (this app)                (server)         (on disk)  │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ✓ No internet required after setup                           │
│   ✓ No API keys needed                                         │
│   ✓ No usage costs                                             │
│   ✓ Complete privacy - your data never leaves your machine     │
│   ✓ Works offline                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| Cloud AI APIs | This Project (Local) |
|---------------|----------------------|
| Requires internet | Works offline |
| Pay per token/request | Free after setup |
| Data sent to servers | Data stays on your machine |
| API keys & accounts | No accounts needed |
| Rate limits | No limits |
| Vendor lock-in | Use any Ollama model |

## Quick Start (5 Minutes)

### Prerequisites

1. **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai/download)

### Installation

```bash
# Step 1: Navigate to the project
cd micro-country

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start Ollama (in a separate terminal)
ollama serve

# Step 4: Pull an AI model (choose one)
ollama pull mistral:7b        # Good general purpose (4GB)
# OR
ollama pull llama3.2          # Faster, smaller (2GB)
# OR
ollama pull qwen2.5:7b        # Recommended for best results (5GB)

# Step 5: Run the system
python orchestrator.py
```

### Your First Interaction

Once running, try these commands:

```
> Design a simple REST API for a todo app

> Write a function to validate email addresses

> /debate Should we use SQL or NoSQL for user data?
```

## Documentation

### For Users

| Document | Description |
|----------|-------------|
| [Quick Start Guide](docs/QUICK_START.md) | 10 hands-on examples to get started |
| [Step-by-Step Tutorial](docs/STEP_BY_STEP_TUTORIAL.md) | 15 progressive exercises with detailed guidance |
| [User Guide](docs/USER_GUIDE.md) | Complete user manual with all features |
| [Installation Guide](docs/INSTALLATION.md) | Detailed setup for all platforms |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Solutions to common problems |
| [Glossary](docs/GLOSSARY.md) | All terms explained |

### For Developers

| Document | Description |
|----------|-------------|
| [Developer Guide](docs/DEVELOPER_GUIDE.md) | Technical deep-dive and development workflows |
| [For Traditional Developers](docs/GETTING_STARTED_FOR_TRADITIONAL_DEVELOPERS.md) | Guide for C/C++/Java developers new to Python |
| [Concepts Explained](docs/CONCEPTS_EXPLAINED.md) | Deep-dive into async, MCP, SQLite, LLMs |
| [Architecture](docs/ARCHITECTURE.md) | System design and component relationships |
| [API Reference](docs/API_REFERENCE.md) | Complete tool and resource documentation |
| [CLAUDE.md](CLAUDE.md) | Quick reference for AI-assisted development |

## Project Structure

```
micro-country/
├── orchestrator.py      # The "brain" - routes your requests
├── config.yaml          # Settings you can customize
├── genius/              # The reasoning system
├── ministries/          # The specialist teams
├── shared/              # Database and shared tools
├── bridge/              # Connects to the AI model
└── tests/               # Verification tests
```

## The Six Ministries

| Ministry | What They Do | Specialists |
|----------|--------------|-------------|
| **Code** | Build software | Architect, Coder, Debugger |
| **Research** | Find information | Analyst, Writer, Searcher |
| **Quality** | Ensure correctness | Tester, Auditor, Validator |
| **Operations** | Manage systems | File Manager, Shell Runner, Deployer |
| **Archives** | Remember decisions | Memory, Indexer |
| **Communications** | Coordinate work | Messenger, Scheduler |

## Key Concepts

### The Genius Protocol

Every specialist thinks in 7 steps before answering:

1. **OBSERVE** - Understand the question
2. **THINK** - Reason through options
3. **REFLECT** - Check understanding
4. **CRITIQUE** - Find potential problems
5. **REFINE** - Improve the approach
6. **ACT** - Provide the answer
7. **VERIFY** - Confirm quality

### The Evidence Court

When specialists disagree, evidence decides:
- **Empirical** (data, tests) beats everything
- **Precedent** (what worked before) beats theory
- **Theory** (logic) beats intuition

## System Requirements

- **OS**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: 16GB minimum (32GB recommended)
- **Disk**: 20GB free space (for AI model)
- **Python**: 3.11 or higher
- **GPU**: Recommended for fast inference (see below)

### GPU/Model Sizing Guide

For best performance, choose a model that fits in your GPU's VRAM:

| GPU VRAM | Recommended Model | Expected Speed |
|----------|-------------------|----------------|
| 4 GB | mistral:7b | ~15-20 tokens/sec |
| 6-8 GB | qwen2.5:7b | ~20-30 tokens/sec |
| 12+ GB | qwen2.5:14b | ~15-25 tokens/sec |
| No GPU | llama3.2 (2GB) | ~5-10 tokens/sec |

**Important**: If your model is larger than your GPU's VRAM, it will run mostly on CPU and be very slow (4-5 tokens/sec). Use a smaller model for better performance.

## Getting Help

1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Read the [FAQ section](docs/USER_GUIDE.md#faq)
3. Review error messages carefully - they often explain the problem

## Acknowledgments

1. This work was inspired by the phrase "country of geniuses in a datacenter" in the essay [The Adolescence of Technology](https://www.darioamodei.com/essay/the-adolescence-of-technology) by Dario Amodei.

2. All code and documentation were generated by [Claude Code](https://claude.ai/claude-code) powered by Claude Opus 4.5.

## License

MIT License - See LICENSE file for details.

---

**Ready to start?** Jump to the [Quick Start Guide](docs/QUICK_START.md) for hands-on examples!
