#!/usr/bin/env python3
"""User prompt submit hook - logs user prompts with lightweight tracking"""
import sys
import json
import os
from datetime import datetime
from pathlib import Path

def main():
    # Lightweight logging of user prompts
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "user_prompt_submit",
        "prompt_length": len(sys.argv[1]) if len(sys.argv) > 1 else 0,
        "platform": "windows",
        "environment": "local_flywheel"
    }
    
    # Log to hooks.jsonl if desired - use Windows path
    try:
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "hooks.jsonl"
        
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Fail silently

if __name__ == "__main__":
    main()