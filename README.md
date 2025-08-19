# Claude Code Configuration

Universal Claude Code configuration system with Windows compatibility, git routing, and spec-driven development workflow.

## Features

- **Universal Compatibility**: Works on Windows, WSL, macOS, and Linux
- **Parallel Multi-Agent Workflows**: Optimized for concurrent agent execution following Anthropic best practices
- **Git Routing System**: Automatic separation of Claude config files from project code
- **Spec-Driven Development**: Complete workflow for feature specifications and tracking
- **WordPress Integration**: Specialized agents for Genesis themes and WordPress development
- **Local Development Support**: Configured for Local by Flywheel and similar environments

## Quick Setup

### 1. Clone Configuration

```bash
# Clone to your user Claude directory
git clone https://github.com/jlpg29/claude.git ~/.claude

# Or on Windows with PowerShell:
git clone https://github.com/jlpg29/claude.git "$env:USERPROFILE\.claude"
```

### 2. Platform-Specific Setup

Run this prompt in Claude Code to automatically configure for your platform:

```
I need you to set up my Claude Code configuration for my current platform. I've just cloned the configuration from GitHub to my ~/.claude directory (or %USERPROFILE%\.claude on Windows).

Please:
1. Detect my current platform (Windows/WSL/macOS/Linux)
2. Update all file paths in the configuration to match my system
3. Configure the git routing system for my environment  
4. Set up any platform-specific hooks or utilities
5. Test that all commands and agents work correctly

The configuration should work with:
- Local development environments (Local by Flywheel, XAMPP, etc.)
- Cross-platform file paths and commands
- Git repositories with proper commit routing
- Spec-driven development workflow

Make sure everything is configured correctly for my specific setup.
```

## Configuration Structure

```
~/.claude/
├── settings.json                    # User-level Claude settings
├── commands/                        # Global slash commands
│   ├── setup-project.md
│   ├── prime.md
│   ├── analyze-codebase.md
│   ├── research-tech.md
│   ├── create-agent.md
│   ├── test-setup.md
│   ├── spec-create.md
│   ├── spec-work.md
│   ├── spec-requirements.md
│   ├── spec-design.md
│   ├── spec-tasks.md
│   └── spec-status.md
├── agents/                          # Global specialized agents
│   ├── meta-agent.md
│   ├── codebase-analyzer.md
│   ├── project-initializer.md
│   └── tech-researcher.md
├── templates/                       # Spec templates
│   └── specs/
│       ├── requirements.template.md
│       ├── design.template.md
│       ├── tasks.template.md
│       └── status.template.json
└── hooks/                          # Git hooks and utilities
    ├── user_prompt_submit.py
    └── utils/
        ├── git_commit_branch_router.py
        ├── git_commit_post_manager.py
        └── coordination.py
```

## Key Commands

### Global Commands
- `/setup-project` - Initialize Claude Code for new/existing projects
- `/prime` - Load project context and prepare Claude for work
- `/analyze-codebase` - Deep analysis of codebase structure
- `/research-tech` - Research technologies and frameworks

### Spec-Driven Development
- `/spec-create [feature-name]` - Create new feature specification
- `/spec-work [feature-name]` - Load existing feature context
- `/spec-requirements [feature-name]` - Generate detailed requirements
- `/spec-design [feature-name]` - Create technical design
- `/spec-tasks [feature-name]` - Break down implementation
- `/spec-status [feature-name]` - Show feature status and progress

## Git Routing System

Automatically separates Claude configuration files from project code:

- **Claude files** (`.claude/`, `CLAUDE.md`) → `claude-spec-files` branch (local only)
- **Project files** → Main project branches (pushed to remote)
- **Mixed commits** → Automatically split into separate commits

### Features:
- Cross-platform compatibility (Windows/WSL/Unix)
- Instance isolation to prevent conflicts
- Comprehensive logging and monitoring
- Safety checks and rollback procedures

## Specialized Agents

### WordPress Development
- **genesis-theme-specialist**: Genesis Framework and child theme development
- **performance-optimizer**: Core Web Vitals and WP Rocket optimization
- **migration-specialist**: Plugin migrations (Feast to Tasty Recipes)
- **test-automation-engineer**: Playwright testing for WordPress

### General Development
- **meta-agent**: Creates new specialized agents with parallel execution design
- **codebase-analyzer**: Deep code structure analysis
- **project-initializer**: Sets up new project configurations
- **tech-researcher**: Researches technologies and creates documentation
- **workflow-coordinator**: Orchestrates parallel multi-agent workflows

## Parallel Multi-Agent Workflows

This configuration is optimized for concurrent agent execution following Anthropic's best practices:

### Concurrent Analysis Pattern
```
Launch multiple agents simultaneously for comprehensive analysis:
- codebase-analyzer: Code structure and patterns
- tech-researcher: Current best practices  
- performance-optimizer: Performance metrics
- security-auditor: Security considerations
```

### Parallel Development Workflow
```
1. Concurrent Planning:
   - requirements-analyst + technical-architect + risk-assessor
   
2. Parallel Implementation:
   - frontend-developer + backend-developer + test-engineer
   
3. Concurrent Validation:
   - code-reviewer + performance-tester + security-auditor
```

### Batch Processing Pattern
```
Group related operations in single requests:
- Multiple file reads across different directories
- Parallel searches for different patterns
- Concurrent data processing tasks
```

### Optimization Benefits
- **Maximum Efficiency**: Multiple agents work simultaneously
- **Reduced Context Usage**: Batched operations minimize API calls
- **Clear Boundaries**: Each agent has distinct, non-overlapping responsibilities
- **Clean Data Handoffs**: Structured interfaces between agent outputs

## Environment Support

### Local Development
- **Local by Flywheel**: WordPress local development with SSL
- **XAMPP/WAMP**: Traditional LAMP stack setups
- **Docker**: Containerized development environments
- **Custom setups**: Adaptable to any local environment

### Platforms
- **Windows**: Native Windows paths and commands
- **WSL**: Windows Subsystem for Linux compatibility
- **macOS**: Unix-style paths and commands
- **Linux**: Full Linux compatibility

## Getting Started

1. **Clone this repository** to your Claude configuration directory
2. **Run the setup prompt** in Claude Code (see above)
3. **Navigate to a project** and use `/prime` to load context
4. **Start spec-driven development** with `/spec-create [feature-name]`

## WordPress-Specific Setup

For WordPress projects with Local by Flywheel:

```
I'm working on a WordPress project with Local by Flywheel. Please:
1. Set up project-specific Claude configuration
2. Configure WordPress-specific agents
3. Set up Playwright testing for the local environment
4. Create any WordPress-specific commands or workflows

My local site details:
- URL: https://[sitename].local  
- Project path: [path to local site]
- Environment: Local by Flywheel
```

## Contributing

This configuration system is designed to be:
- **Modular**: Easy to add new agents and commands
- **Extensible**: Simple to customize for specific workflows
- **Cross-platform**: Works on any development environment
- **Version-controlled**: Track changes and share improvements

Feel free to customize agents, commands, and templates for your specific needs.