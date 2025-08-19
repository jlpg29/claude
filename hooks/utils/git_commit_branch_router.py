#!/usr/bin/env python3
"""
Git Commit Branch Router - Windows Version
Routes commits to appropriate branches based on file types
ISOLATED from WSL to prevent authentication conflicts
"""
import sys
import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

# Windows-specific configuration to prevent WSL conflicts
WINDOWS_CLAUDE_IDENTIFIER = "windows-claude-instance"
LOG_PREFIX = "[WIN-GIT-ROUTER]"

def log_action(action, details=None):
    """Log git routing actions with Windows identifier"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "git_commit_routing",
        "action": action,
        "details": details or {},
        "platform": "windows",
        "claude_instance": WINDOWS_CLAUDE_IDENTIFIER
    }
    
    try:
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "git-routing-windows.jsonl"
        
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass

def run_git_command(cmd, capture_output=True):
    """Run git command with Windows compatibility"""
    try:
        # Use Windows-compatible git execution
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            env={**os.environ, "CLAUDE_INSTANCE": WINDOWS_CLAUDE_IDENTIFIER}
        )
        return result
    except Exception as e:
        log_action("git_command_error", {"command": cmd, "error": str(e)})
        return None

def get_staged_files():
    """Get list of staged files"""
    result = run_git_command("git diff --cached --name-only")
    if result and result.returncode == 0:
        return [f.strip() for f in result.stdout.split('\n') if f.strip()]
    return []

def is_claude_file(filepath):
    """Check if file is Claude-related"""
    claude_patterns = [
        '.claude/',
        'CLAUDE.md',
        '.claude\\',  # Windows path separator
    ]
    return any(pattern in filepath for pattern in claude_patterns)

def get_current_branch():
    """Get current git branch"""
    result = run_git_command("git branch --show-current")
    if result and result.returncode == 0:
        return result.stdout.strip()
    return None

def branch_exists(branch_name):
    """Check if branch exists"""
    result = run_git_command(f"git show-ref --verify --quiet refs/heads/{branch_name}")
    return result and result.returncode == 0

def create_claude_spec_branch():
    """Create claude-spec-files branch if it doesn't exist"""
    if not branch_exists("claude-spec-files"):
        # Create orphan branch for Claude files
        run_git_command("git checkout --orphan claude-spec-files")
        run_git_command("git rm -rf .")
        
        # Create initial commit
        initial_readme = Path(".claude/README-WINDOWS.md")
        initial_readme.parent.mkdir(parents=True, exist_ok=True)
        initial_readme.write_text(
            f"# Windows Claude Code Configuration\n\n"
            f"This branch contains Claude Code configurations for Windows instance.\n"
            f"Created: {datetime.now().isoformat()}\n"
            f"Instance: {WINDOWS_CLAUDE_IDENTIFIER}\n"
        )
        
        run_git_command("git add .claude/README-WINDOWS.md")
        run_git_command(f'git commit -m "Initialize Windows Claude configuration branch"')
        
        log_action("created_claude_branch")

def setup_windows_worktree():
    """Set up Windows-specific git worktree system"""
    project_root = Path.cwd()
    worktree_path = project_root.parent / f".{project_root.name}-claude-windows"
    
    # Check if worktree already exists
    result = run_git_command("git worktree list")
    if result and str(worktree_path) in result.stdout:
        log_action("worktree_exists", {"path": str(worktree_path)})
        return str(worktree_path)
    
    # Create claude-spec-files branch if needed
    create_claude_spec_branch()
    
    # Go back to original branch
    original_branch = get_current_branch()
    if original_branch != "claude-spec-files":
        run_git_command(f"git checkout {original_branch}")
    
    # Create worktree
    if not worktree_path.exists():
        result = run_git_command(f'git worktree add "{worktree_path}" claude-spec-files')
        if result and result.returncode == 0:
            log_action("created_worktree", {"path": str(worktree_path)})
            
            # Create Windows-specific symlink
            symlink_target = project_root / ".claude"
            symlink_source = worktree_path / ".claude"
            
            try:
                if symlink_target.exists() and symlink_target.is_symlink():
                    symlink_target.unlink()
                
                # Create Windows symlink (requires admin or dev mode)
                subprocess.run([
                    "cmd", "/c", "mklink", "/D", 
                    str(symlink_target), str(symlink_source)
                ], check=True)
                
                log_action("created_symlink", {
                    "target": str(symlink_target),
                    "source": str(symlink_source)
                })
            except Exception as e:
                log_action("symlink_error", {"error": str(e)})
    
    return str(worktree_path)

def route_commit():
    """Main routing logic"""
    staged_files = get_staged_files()
    if not staged_files:
        return
    
    current_branch = get_current_branch()
    claude_files = [f for f in staged_files if is_claude_file(f)]
    code_files = [f for f in staged_files if not is_claude_file(f)]
    
    log_action("analyzing_commit", {
        "current_branch": current_branch,
        "total_files": len(staged_files),
        "claude_files": len(claude_files),
        "code_files": len(code_files)
    })
    
    # Set up worktree system
    worktree_path = setup_windows_worktree()
    
    if claude_files and code_files:
        # Mixed commit - split it
        log_action("splitting_mixed_commit")
        
        # First, unstage code files and commit Claude files
        for code_file in code_files:
            run_git_command(f'git reset HEAD "{code_file}"')
        
        # Switch to claude-spec-files branch via worktree
        os.chdir(worktree_path)
        
        # Stage and commit Claude files
        for claude_file in claude_files:
            run_git_command(f'git add "{claude_file}"')
        
        commit_msg = f"Windows Claude: Update configuration files\n\nFiles: {', '.join(claude_files)}\nInstance: {WINDOWS_CLAUDE_IDENTIFIER}"
        run_git_command(f'git commit -m "{commit_msg}"')
        
        # Return to original directory and branch
        os.chdir(str(Path(worktree_path).parent / Path(worktree_path).name.replace('.', '').replace('-claude-windows', '')))
        
        # Re-stage code files for separate commit
        for code_file in code_files:
            run_git_command(f'git add "{code_file}"')
        
        log_action("split_commit_completed")
        
    elif claude_files and not code_files:
        # Only Claude files - route to claude-spec-files branch
        log_action("routing_claude_only")
        
        # Switch to claude-spec-files branch via worktree
        original_dir = os.getcwd()
        os.chdir(worktree_path)
        
        # Stage and commit Claude files
        for claude_file in claude_files:
            run_git_command(f'git add "{claude_file}"')
        
        commit_msg = f"Windows Claude: Update configuration files\n\nFiles: {', '.join(claude_files)}\nInstance: {WINDOWS_CLAUDE_IDENTIFIER}"
        run_git_command(f'git commit -m "{commit_msg}"')
        
        # Return to original directory
        os.chdir(original_dir)
        
        # Reset the original staging area since we committed elsewhere
        for claude_file in claude_files:
            run_git_command(f'git reset HEAD "{claude_file}"')
        
        log_action("claude_commit_completed")
        sys.exit(0)  # Prevent double commit
    
    # If only code files, let normal commit proceed
    log_action("allowing_code_commit")

def main():
    """Main entry point"""
    try:
        # Only run if in a git repository
        if not Path(".git").exists():
            return
        
        # Check if we're in the correct project
        if "lees-supper-club" not in str(Path.cwd()):
            return
        
        # Run routing logic
        route_commit()
        
    except Exception as e:
        log_action("routing_error", {"error": str(e)})

if __name__ == "__main__":
    main()