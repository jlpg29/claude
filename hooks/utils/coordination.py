#!/usr/bin/env python3
"""
Hook Coordination Utilities - Windows Version
Coordinates hook execution and prevents conflicts with WSL
"""
import os
import json
from datetime import datetime
from pathlib import Path

WINDOWS_CLAUDE_IDENTIFIER = "windows-claude-instance"
WSL_CLAUDE_IDENTIFIER = "wsl-claude-instance"

def is_wsl_environment():
    """Check if running in WSL (should return False for Windows)"""
    return "microsoft" in str(os.uname().release).lower() if hasattr(os, 'uname') else False

def get_claude_instance_id():
    """Get the Claude instance identifier"""
    if is_wsl_environment():
        return WSL_CLAUDE_IDENTIFIER
    return WINDOWS_CLAUDE_IDENTIFIER

def should_execute_hook(hook_name):
    """Determine if hook should execute based on environment"""
    instance_id = get_claude_instance_id()
    
    # Windows Claude should only execute Windows-specific hooks
    if instance_id == WINDOWS_CLAUDE_IDENTIFIER:
        return True
    
    # WSL Claude should only execute WSL-specific hooks
    return False

def log_hook_coordination(action, details=None):
    """Log hook coordination decisions"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "hook_coordination",
        "action": action,
        "details": details or {},
        "claude_instance": get_claude_instance_id(),
        "platform": "windows" if get_claude_instance_id() == WINDOWS_CLAUDE_IDENTIFIER else "wsl"
    }
    
    try:
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"hook-coordination-{get_claude_instance_id()}.jsonl"
        
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass

def prevent_api_conflicts():
    """Prevent API authentication conflicts between Windows and WSL"""
    instance_id = get_claude_instance_id()
    
    # Set environment variables to isolate instances
    os.environ["CLAUDE_INSTANCE_ID"] = instance_id
    os.environ["CLAUDE_CONFIG_ISOLATION"] = "true"
    
    # Different token storage paths to prevent conflicts
    if instance_id == WINDOWS_CLAUDE_IDENTIFIER:
        os.environ["CLAUDE_TOKEN_PATH"] = str(Path.home() / ".claude" / "tokens-windows.json")
    
    log_hook_coordination("api_isolation_configured", {"instance_id": instance_id})