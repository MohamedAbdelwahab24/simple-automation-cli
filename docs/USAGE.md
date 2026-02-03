# Simple Automation CLI - Usage Guide

## Installation

### Method 1: Quick Install (Recommended)

```bash
chmod +x install.sh
./install.sh
```

### Method 2: Python Installation

```bash
pip install -e .
```

## Commands

### 1. Backup Command

Backup database tables quickly and easily.

```bash
# Backup PostgreSQL database
automation-cli backup --db postgres --table users

# Backup MySQL database
automation-cli backup --db mysql --table customers
```

**Output:**
```
📦 Starting backup: postgres
🧰 Table: users
⏰ Started at: 2026-02-03 10:00:00
  Connecting to database...
  Checking connection...
  Starting backup...
  Backup completed successfully ✓
💾 Backup saved to: /backups/postgres_users_20260203.sql
```

### 2. Deploy Command

Deploy applications with health checks.

```bash
# Deploy to production
automation-cli deploy --service api --env production

# Deploy to staging with custom URL
automation-cli deploy --service web --env staging --url https://staging.example.com
```

**Output:**
```
🚀 Deploying: api
🔧 Environment: production
🔄 Building Docker image...
  Pulling latest code...
  Building Docker image...
  Running migrations...
  Starting containers...
  Health checks passed ✓
🌐 Service available at: https://api.example.com
```

### 3. Test Command

Run automated tests.

```bash
# Run all tests
automation-cli test
```

**Output:**
```
🧪 Running tests...
  Unit tests... ✓
  Integration tests... ✓
  Performance tests... ✓
✅ All tests passed!
```

### 4. Version Command

Check version information.

```bash
automation-cli --version
# Output: Simple Automation CLI v1.0.0
```

## Configuration

The CLI stores configuration in:

- **Install location**: `~/.local/bin/automation-cli`
- **Python package**: `src/main.py`
- **Source location**: Current directory

## Extending

To add new commands:

1. Edit `src/main.py`
2. Add new methods to `AutomationCLI` class
3. Update `argparse` section in `main()`
4. Test locally: `python src/main.py`

## License

MIT License - See LICENSE file for details
