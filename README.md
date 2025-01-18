# Obsidian Markdown

A tool to parse obsidian markdown note into a abstract syntax tree (AST) and then render to regular markdown or other formats.

## TODO LIST

### Global Tasks

- [x] Use uv to manage the project
- [x] Use pytest to write test cases
- [ ] Main class (`ObsidianMarkdown`)
- [ ] parse method (`ObsidianMarkdown.parse`)
- [ ] render method (`ObsidianMarkdown.parse`)

### Block Parsers

- [x] front matter block
- [x] Paragraph
- [-] image link, including internal and external link styles
- [x] Section block, based on heading level
- [x] quote block
- [x] code block, use the same method as other blocks to parse
- [x] math block
- [x] call out
- [x] list block, including ordered, unordered, and task list
- [x] horizontal rule
- [x] footnote block
- [x] comments block(%% %%), which is only visible in editing view
- [x] tables
- [ ] [link to a block](https://help.obsidian.md/Linking+notes+and+files/Internal+links#Link+to+a+block+in+a+note)

### Inline Parsers

- [ ] bold
- [ ] italic
- [ ] highlight
- [ ] Strikethroughs
- [ ] internal link
- [ ] external link
- [ ] inline code
- [ ] inline footnote mark
- [ ] inline comments

### Default Render

### Hugo Render
