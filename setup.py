import os
import shutil
from pathlib import Path

# Paths (Configured for OpenCode - Modify if using Claude Code or another agent)
agent_config_dir = Path.home() / ".config" / "opencode"
active_skills_dir = agent_config_dir / "skills"

# This must be totally outside the agent's recursive scanning path!
hidden_library_dir = Path.home() / ".opencode-skill-libraries"

def main():
    print("Welcome to SkillPointer Automated Setup 🎯")
    print("------------------------------------------")
    
    if not active_skills_dir.exists():
        print(f"Error: Active skills directory not found at {active_skills_dir}")
        print("Please edit the source code if your agent uses a different path.")
        return

    hidden_library_dir.mkdir(parents=True, exist_ok=True)

    # Categories structure (Customize these lists to match your specific skills)
    categories = {
        "animation": ["animation", "motion", "transitions", "bounce"],
        "prompt-engineering": ["prompt", "llm", "ai-engineer", "persona", "reasoning"],
        "web-dev": ["react", "vue", "angular", "css", "html", "tailwind", "frontend", "web"],
        "backend-dev": ["node", "express", "django", "python", "api", "graphql", "backend", "go", "rust"],
        "database": ["sql", "mysql", "postgres", "mongo", "redis", "database", "schema"],
        "devops": ["docker", "kubernetes", "aws", "deploy", "ci-cd", "github-actions", "devops"],
        "testing": ["jest", "cypress", "playwright", "test", "qa"],
        "security": ["security", "auth", "crypto", "oauth"],
        "game-dev": ["game", "unity", "unreal", "godot", "phaser"],
        "architecture": ["architecture", "design-pattern", "solid", "clean-code"]
    }

    moved_count = 0
    category_counts = {cat: 0 for cat in categories.keys()}
    category_counts["general-coding"] = 0

    print("Scanning active skills...")
    for folder in list(active_skills_dir.iterdir()):
        if not folder.is_dir():
            continue
            
        # Don't move things we've already generated as pointers
        if folder.name.endswith("-category-pointer"):
            continue

        name_lower = folder.name.lower()
        
        # Determine the matched category based on keyword matching
        matched_category = "general-coding"
        for cat, keywords in categories.items():
            if any(kw in name_lower for kw in keywords):
                matched_category = cat
                break
                
        # Move the skill folder into the hidden library subfolder
        cat_dir = hidden_library_dir / matched_category
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        dest = cat_dir / folder.name
        if dest.exists():
            shutil.rmtree(dest)
            
        shutil.move(str(folder), str(cat_dir))
        category_counts[matched_category] += 1
        moved_count += 1

    print(f"\nMoved {moved_count} skills into the hidden library folder: {hidden_library_dir}")

    # Generate the Pointer Skills
    # This template is highly optimized for AI consumption. Do not alter the core instructions.
    pointer_template = """---
name: {category_name}-category-pointer
description: Triggers when encountering any task related to {category_name}. This is a pointer to a library of specialized skills.
---

# {category_title} Capability Library 🎯

You do not have all {category_title} skills loaded immediately in your background context. Instead, you have access to a rich library of {count} highly-specialized skills on your local filesystem.

## Instructions
1. When you need to perform a task related to {category_name}, you MUST use your file reading tools (like `list_dir` and `view_file` or `read_file`) to browse the hidden library directory: `{library_path}`
2. Locate the specific Markdown files related to the exact sub-task you need (e.g., if you need to build an API, find the API design skill).
3. Read the relevant Markdown file(s) into your context.
4. Follow the specific instructions and best practices found within those files to complete the user's request.

## Available Knowledge
This library contains {count} specialized skills covering various aspects of {category_title}.

**Hidden Library Path:** `{library_path}`

*Reminder: Do not guess best practices or blindly search GitHub. Always consult your local library files first.*
"""

    for cat, count in category_counts.items():
        if count == 0:
            continue
            
        cat_dir = hidden_library_dir / cat
        pointer_name = f"{cat}-category-pointer"
        pointer_dir = active_skills_dir / pointer_name
        pointer_dir.mkdir(parents=True, exist_ok=True)
        
        cat_title = cat.replace("-", " ").title()
        
        content = pointer_template.format(
            category_name=cat,
            category_title=cat_title,
            count=count,
            library_path=str(cat_dir)
        )
        
        with open(pointer_dir / "SKILL.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Created Pointer Skill for Category: {cat} (Points to {count} hidden skills)")

    print("\nHierarchical refactoring complete!")
    print(f"Your active skills directory now only contains generic Pointer Skills instead of massive raw skills.")
    print("Enjoy your infinite context window! 🚀")

if __name__ == "__main__":
    main()
