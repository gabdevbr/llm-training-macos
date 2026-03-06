# Contributing to LLM Training macOS

Thanks for interest in contributing! This project is open to contributions.

## What We Need

- ✅ Bug fixes
- ✅ New templates (support agent, research assistant, etc)
- ✅ Better documentation
- ✅ Performance improvements
- ✅ Example datasets
- ✅ Integration helpers (OpenClaw, Langchain, etc)

## How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR-USERNAME/llm-training-macos.git
cd llm-training-macos
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow existing code style
- Add comments for complex logic
- Test locally before pushing

### 3. Commit
```bash
git commit -m "feat: add new template for research assistant"
# or
git commit -m "fix: dataset loading on Windows"
# or
git commit -m "docs: improve CONTRIBUTING.md"
```

Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

### 4. Push & Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Why this matters
- Any testing you did

## Code Style

- Python: PEP 8 (use `black` for formatting)
- Scripts: bash best practices
- Docs: Markdown, clear and concise

## Adding a New Template

1. Create folder: `templates/your-template/`
2. Add sample dataset: `templates/your-template/dataset.jsonl`
3. Add README: `templates/your-template/README.md`
4. Update main README with your template
5. Test it works end-to-end

## Community

- Issues: Report bugs or request features
- Discussions: Ask questions, share ideas
- Examples: Share what you built!

---

**Thank you for contributing!** 🙌
