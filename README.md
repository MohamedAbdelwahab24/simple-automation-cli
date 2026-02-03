# Simple Automation CLI 🚀

Fast, production-ready automation tools for data engineering tasks.

## Features

✅ Quick setup (1 minute)  
✅ Clear, structured output  
✅ Safer defaults and validation  
✅ Easy to extend

## Quick Start

```bash
# Install (simple script, no dependencies)
./install.sh

# Use commands
automation-cli --help
automation-cli backup --db postgres --table users
automation-cli deploy --service api
automation-cli test
```

## Usage

### Backup

```bash
automation-cli backup --db postgres --table users
automation-cli backup --db postgres --table users --output-dir ./backups --compress
automation-cli backup --db postgres --table users --dry-run
```

### Deploy

```bash
automation-cli deploy --service api --env production
automation-cli deploy --service api --env staging --image-tag 1.2.3
automation-cli deploy --service api --dry-run
```

### Test

```bash
automation-cli test
automation-cli test --suite unit
```

## Installation

```bash
chmod +x install.sh
./install.sh
```

## License

MIT License - Free to use, modify, and distribute
