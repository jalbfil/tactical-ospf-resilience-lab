"""
Collect evidence from Cisco IOS routers using SSH/Netmiko.

This script is prepared for Phase 2 of the lab. Packet Tracer may not support
external SSH automation depending on the topology and version. The same logic is
valid for GNS3, EVE-NG, Cisco IOSv or real IOS devices.

Usage:
    1. Copy .env.example to .env
    2. Set ROUTER_USERNAME and ROUTER_PASSWORD
    3. Adjust ROUTERS if needed
    4. Run: python collect_evidence.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
import os


OUTPUT_DIR = Path("evidence/automation")

COMMANDS: List[str] = [
    "show clock",
    "show ip interface brief",
    "show ip ospf neighbor",
    "show ip route ospf",
    "show ip route 192.168.3.1",
    "traceroute 192.168.3.1",
]

# Replace host values with the management IPs of your lab devices.
ROUTERS: List[Dict[str, str]] = [
    {"name": "BASE", "host": "192.168.1.1"},
    {"name": "HELI-ALFA", "host": "192.168.2.1"},
    {"name": "HELI-BRAVO", "host": "192.168.3.1"},
    {"name": "HELI-CHARLIE", "host": "192.168.4.1"},
]


def build_device(router: Dict[str, str], username: str, password: str) -> Dict[str, str]:
    return {
        "device_type": "cisco_ios",
        "host": router["host"],
        "username": username,
        "password": password,
        "fast_cli": False,
    }


def collect_from_router(router: Dict[str, str], username: str, password: str) -> str:
    device = build_device(router, username, password)
    output_sections: List[str] = []

    try:
        with ConnectHandler(**device) as connection:
            for command in COMMANDS:
                output_sections.append(f"\n\n### {command}\n")
                output_sections.append(connection.send_command(command, read_timeout=30))
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as exc:
        output_sections.append(f"ERROR connecting to {router['name']} ({router['host']}): {exc}")
    except Exception as exc:  # Defensive catch for lab environments
        output_sections.append(f"UNEXPECTED ERROR on {router['name']} ({router['host']}): {exc}")

    return "\n".join(output_sections)


def main() -> None:
    load_dotenv()

    username = os.getenv("ROUTER_USERNAME")
    password = os.getenv("ROUTER_PASSWORD")

    if not username or not password:
        raise RuntimeError("ROUTER_USERNAME and ROUTER_PASSWORD must be set in .env")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = OUTPUT_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    for router in ROUTERS:
        print(f"Collecting evidence from {router['name']}...")
        output = collect_from_router(router, username, password)
        output_file = run_dir / f"{router['name']}.txt"
        output_file.write_text(output, encoding="utf-8")

    print(f"Evidence saved in: {run_dir}")


if __name__ == "__main__":
    main()
