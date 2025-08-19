#!/usr/bin/env python3
"""
Git Post-Commit Manager - Windows Version
Handles post-commit logging and safety checks
ISOLATED from WSL to prevent authentication conflicts
"""
import sys
import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

WINDOWS_CLAUDE_IDENTIFIER = "windows-claude-instance"

def log_action(action, details=None):
    """Log post-commit actions with Windows identifier"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "git_post_commit",
        "action": action,
        "details": details or {},
        "platform": "windows",
        "claude_instance": WINDOWS_CLAUDE_IDENTIFIER
    }
    
    try:
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "git-post-commit-windows.jsonl"
        
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass

def run_git_command(cmd):
    """Run git command with Windows compatibility"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            env={**os.environ, "CLAUDE_INSTANCE": WINDOWS_CLAUDE_IDENTIFIER}
        )
        return result
    except Exception as e:
        log_action("git_command_error", {"command": cmd, "error": str(e)})
        return None

def get_current_branch():
    """Get current git branch"""
    result = run_git_command("git branch --show-current")
    if result and result.returncode == 0:
        return result.stdout.strip()
    return None

def get_last_commit_info():
    """Get information about the last commit"""
    result = run_git_command("git log -1 --pretty=format:'%H|%s|%an|%ad' --date=iso")
    if result and result.returncode == 0:
        parts = result.stdout.split('|')
        if len(parts) >= 4:
            return {
                "hash": parts[0],
                "message": parts[1],
                "author": parts[2],
                "date": parts[3]
            }
    return None

def check_for_claude_spec_files_push():
    """Prevent accidental push of claude-spec-files branch"""
    current_branch = get_current_branch()
    
    if current_branch == "claude-spec-files":
        print(f"\n{chr(9888)} WARNING: You are on the 'claude-spec-files' branch!")
        print("This branch should NOT be pushed to remote repositories.")
        print("It contains local Claude configuration and should remain local only.")
        print(f"Windows Claude Instance: {WINDOWS_CLAUDE_IDENTIFIER}\n")
        
        log_action("claude_branch_warning", {"branch": current_branch})

def check_uncommitted_changes():
    """Check for remaining uncommitted changes"""
    result = run_git_command("git status --porcelain")
    if result and result.stdout.strip():
        uncommitted = result.stdout.strip().split('\n')
        print(f"\nNote: You have {len(uncommitted)} uncommitted changes remaining:")
        for change in uncommitted[:5]:  # Show first 5
            print(f"  {change}")
        if len(uncommitted) > 5:
            print(f"  ... and {len(uncommitted) - 5} more")
        print()
        
        log_action("uncommitted_changes_detected", {"count": len(uncommitted)})

def main():
    """Main post-commit handler"""
    try:
        # Only run if in a git repository
        if not Path(".git").exists():
            return
        
        # Check if we're in the correct project
        if "lees-supper-club" not in str(Path.cwd()):
            return
        
        current_branch = get_current_branch()
        commit_info = get_last_commit_info()
        
        log_action("post_commit_executed", {
            "branch": current_branch,
            "commit_info": commit_info
        })
        
        # Safety checks
        check_for_claude_spec_files_push()
        check_uncommitted_changes()
        
        # Success message
        if current_branch and commit_info:
            print(f"✅ Commit successful on branch '{current_branch}'")
            print(f"   {commit_info['hash'][:8]}: {commit_info['message']}")
            print(f"   Windows Claude Instance: {WINDOWS_CLAUDE_IDENTIFIER}")
        
    except Exception as e:
        log_action("post_commit_error", {"error": str(e)})

if __name__ == "__main__":
    main()