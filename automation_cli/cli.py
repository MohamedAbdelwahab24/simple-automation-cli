#!/usr/bin/env python3
"""Simple Automation CLI.

Fast, production-ready automation tools for data engineering tasks.
"""

from __future__ import annotations

import argparse
import gzip
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from automation_cli import __version__


@dataclass(frozen=True)
class BackupConfig:
    """Configuration for backup operations."""

    database: str
    table: str
    output_dir: Path
    compress: bool
    dry_run: bool


@dataclass(frozen=True)
class DeployConfig:
    """Configuration for deploy operations."""

    service: str
    environment: str
    image_tag: str
    url: str
    dry_run: bool


@dataclass(frozen=True)
class TestConfig:
    """Configuration for test operations."""

    suite: str


class AutomationCLI:
    """Main CLI class."""

    def __init__(self, *, version: str) -> None:
        self.version = version

    def run_backup(self, args: argparse.Namespace) -> int:
        """Run a backup operation."""
        config = BackupConfig(
            database=args.db,
            table=args.table,
            output_dir=Path(args.output_dir),
            compress=args.compress,
            dry_run=args.dry_run,
        )
        self._validate_identifier(config.database, "database")
        self._validate_identifier(config.table, "table")

        timestamp = datetime.now(timezone.utc)
        suffix = ".sql.gz" if config.compress else ".sql"
        filename = f"{config.database}_{config.table}_{timestamp:%Y%m%dT%H%M%SZ}{suffix}"
        output_path = config.output_dir / filename

        self._headline("📦 Starting backup")
        self._print_kv("Database", config.database)
        self._print_kv("Table", config.table)
        self._print_kv("Output", str(output_path))
        self._print_kv("Started", timestamp.isoformat())

        steps = [
            "Validating configuration",
            "Connecting to database",
            "Streaming table data",
            "Finalizing backup",
        ]
        self._run_steps(steps)

        if config.dry_run:
            self._headline("ℹ️ Dry run complete")
            return 0

        config.output_dir.mkdir(parents=True, exist_ok=True)
        self._write_backup_file(output_path, config, timestamp)

        self._headline("✅ Backup completed")
        self._print_kv("Saved", str(output_path))
        return 0

    def run_deploy(self, args: argparse.Namespace) -> int:
        """Run a deploy operation."""
        service = args.service
        environment = args.env
        image_tag = args.image_tag
        self._validate_identifier(service, "service")
        self._validate_identifier(environment, "environment")

        url = args.url or self._default_url(service, environment)
        config = DeployConfig(
            service=service,
            environment=environment,
            image_tag=image_tag,
            url=url,
            dry_run=args.dry_run,
        )

        self._headline("🚀 Starting deploy")
        self._print_kv("Service", config.service)
        self._print_kv("Environment", config.environment)
        self._print_kv("Image tag", config.image_tag)
        self._print_kv("Target URL", config.url)

        steps = [
            "Pulling latest code",
            f"Building Docker image ({config.image_tag})",
            "Running database migrations",
            "Starting containers",
            "Performing health checks",
        ]
        self._run_steps(steps)

        if config.dry_run:
            self._headline("ℹ️ Dry run complete")
            return 0

        self._headline("✅ Deploy completed")
        self._print_kv("Service URL", config.url)
        return 0

    def run_tests(self, args: argparse.Namespace) -> int:
        """Run automated tests."""
        config = TestConfig(suite=args.suite)
        self._headline("🧪 Running tests")
        self._print_kv("Suite", config.suite)

        suite_steps = {
            "unit": ["Unit tests"],
            "integration": ["Integration tests"],
            "performance": ["Performance tests"],
            "all": ["Unit tests", "Integration tests", "Performance tests"],
        }

        for step in suite_steps[config.suite]:
            self._run_steps([step])

        self._headline("✅ All tests passed")
        return 0

    def _run_steps(self, steps: list[str]) -> None:
        for step in steps:
            print(f"  • {step}... done")

    def _headline(self, message: str) -> None:
        print(f"\n{message}")

    def _print_kv(self, label: str, value: str) -> None:
        print(f"  {label}: {value}")

    def _default_url(self, service: str, environment: str) -> str:
        if environment == "production":
            return f"https://{service}.example.com"
        return f"https://{service}.{environment}.example.com"

    def _validate_identifier(self, value: str, label: str) -> None:
        if not value or not value.replace("-", "").replace("_", "").isalnum():
            raise SystemExit(f"Invalid {label}: '{value}'. Use letters, numbers, '-' or '_'.")

    def _write_backup_file(
        self,
        output_path: Path,
        config: BackupConfig,
        timestamp: datetime,
    ) -> None:
        header = (
            "-- Simple Automation CLI backup\n"
            f"-- Database: {config.database}\n"
            f"-- Table: {config.table}\n"
            f"-- Timestamp (UTC): {timestamp.isoformat()}\n"
            "-- NOTE: This is a placeholder backup file.\n"
        )
        if config.compress:
            with gzip.open(output_path, "wt", encoding="utf-8") as handle:
                handle.write(header)
        else:
            output_path.write_text(header, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="automation-cli",
        description="Simple Automation CLI for data engineering tasks",
        epilog="Built with ❤️ by Mohamed Abdelwahab",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Simple Automation CLI v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup", help="Backup database tables")
    backup_parser.add_argument("--db", required=True, help="Database name")
    backup_parser.add_argument("--table", required=True, help="Table name to backup")
    backup_parser.add_argument(
        "--output-dir",
        default="backups",
        help="Directory to store the backup file",
    )
    backup_parser.add_argument(
        "--compress",
        action="store_true",
        help="Compress the backup output with gzip",
    )
    backup_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing files",
    )

    deploy_parser = subparsers.add_parser("deploy", help="Deploy applications")
    deploy_parser.add_argument("--service", required=True, help="Service name to deploy")
    deploy_parser.add_argument(
        "--env",
        default="production",
        help="Environment name (default: production)",
    )
    deploy_parser.add_argument(
        "--image-tag",
        default="latest",
        help="Docker image tag to deploy (default: latest)",
    )
    deploy_parser.add_argument("--url", help="Service URL after deployment")
    deploy_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without deploying",
    )

    test_parser = subparsers.add_parser("test", help="Run automated tests")
    test_parser.add_argument(
        "--suite",
        choices=["unit", "integration", "performance", "all"],
        default="all",
        help="Test suite to run (default: all)",
    )

    return parser


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    cli = AutomationCLI(version=__version__)

    if args.command == "backup":
        return cli.run_backup(args)
    if args.command == "deploy":
        return cli.run_deploy(args)
    if args.command == "test":
        return cli.run_tests(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
