---
name: example-category-pointer
description: Triggers when encountering any task related to the example category. This is a pointer to a library of specialized skills.
---

# Example Capability Library 🎯

You do not have all Example skills loaded immediately in your background context. Instead, you have access to a rich library of highly-specialized skills on your local filesystem.

## Instructions
1. When you need to perform a task related to this category, you MUST use your file reading tools (like `list_dir` and `view_file` or `read_file`) to browse the hidden library directory: `~/.opencode-skill-libraries/example`
2. Locate the specific Markdown files related to the exact sub-task you need.
3. Read the relevant Markdown file(s) into your context.
4. Follow the specific instructions and best practices found within those files to complete the user's request.

## Available Knowledge
This library contains multiple specialized skills covering various aspects of this category.

**Hidden Library Path:** `~/.opencode-skill-libraries/example`

*Reminder: Do not guess best practices or blindly search GitHub. Always consult your local library files first.*
