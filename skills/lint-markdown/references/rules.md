# markdownlint Rules Reference

## Non-Fixable Rules (Manual Fix Required)

These rules are NOT auto-fixed by `--fix`. Parse the error output and apply fixes with the Edit tool.

| Rule  | Alias                  | Fix Strategy                                                                               |
| ----- | ---------------------- | ------------------------------------------------------------------------------------------ |
| MD001 | heading-increment      | Adjust heading levels so they increment by one (e.g., `#` -> `##` -> `###`)                |
| MD002 | first-heading-h1       | Change first heading to `#`                                                                |
| MD003 | heading-style          | Make all headings use the same style (atx `#` is standard)                                 |
| MD006 | ul-start-left          | Remove leading indentation from top-level list items                                       |
| MD008 | ul-indent              | Fix unordered list indentation to configured spaces                                        |
| MD012 | no-multiple-blanks     | Collapse consecutive blank lines into one                                                  |
| MD013 | line-length            | Break long lines at word boundaries (default limit: 80)                                    |
| MD024 | no-duplicate-heading   | Rename duplicate headings to be unique                                                     |
| MD025 | single-title           | Keep only one `#` top-level heading per file                                               |
| MD028 | no-blanks-blockquote   | Remove blank lines between consecutive blockquote lines or use a single `>` on blank lines |
| MD033 | no-inline-html         | Replace inline HTML with Markdown equivalents (e.g., `<br>` -> line break, `<b>` -> `**`)  |
| MD035 | hr-style               | Standardize horizontal rules (use `---`)                                                   |
| MD036 | no-emphasis-as-heading | Convert emphasized paragraphs to proper headings                                           |
| MD040 | fenced-code-language   | Add language identifier to fenced code blocks (e.g., ` ```bash `)                          |
| MD041 | first-line-heading     | Ensure file starts with a top-level heading                                                |
| MD042 | no-empty-links         | Add valid URL to empty links                                                               |
| MD043 | required-headings      | Reorder/rename headings to match required structure                                        |
| MD045 | no-alt-text            | Add `alt="description"` to images                                                          |
| MD046 | code-block-style       | Convert code blocks to consistent style (fenced is standard)                               |
| MD048 | code-fence-style       | Standardize fence character (backtick `` ` `` is standard)                                 |
| MD052 | reference-links-images | Define missing reference link labels or convert to inline links                            |
| MD055 | table-pipe-style       | Fix table pipe alignment (leading and trailing pipes)                                      |
| MD056 | table-column-count     | Fix column count so all rows match the header                                              |
| MD058 | blanks-around-tables   | Add blank lines before and after tables                                                    |

## Fixable Rules (Auto-fixed by `--fix`)

These are handled automatically by `markdownlint-cli2 --fix`. No manual intervention needed:

MD004, MD005, MD007, MD009, MD010, MD011, MD014, MD018, MD019, MD020,
MD021, MD022, MD023, MD026, MD027, MD029, MD030, MD031, MD032, MD034,
MD037, MD038, MD039, MD044, MD047, MD049, MD050, MD051, MD053, MD054

## Output Format

Each error line from `markdownlint-cli2` follows this pattern:

```text
<filepath>:<line>[:<column>] <MDXXX>/<alias> <description> [<context>]
```

Example:

```text
file.md:7 MD032/blanks-around-lists Lists should be surrounded by blank lines [Context: "* list item"]
file.md:8:1 MD004/ul-style Unordered list style [Expected: asterisk; Actual: dash]
```

Parse the rule ID (e.g., `MD032`) to determine if the issue is fixable or requires manual editing.
