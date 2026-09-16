# Content reviews

Editorial reviews of the course material — the notes in `notes/` and the syllabus
in `docs/syllabus/`. These are working notes about the content, not part of it.

## Not published

This directory is excluded from the rendered site. Quarto renders every `.md` in
the project by default, so the exclusion is explicit in `_quarto.yml`:

```yaml
project:
  render:
    - "**/*.qmd"
    - "**/*.md"
    - "!docs/reviews/"
```

Without that line a critique of the syllabus would ship to the course website.
If you add a review and want to confirm it stays private:

```bash
pixi run render
ls _site/docs/reviews    # should not exist
```

(GitHub still renders this directory in the repo view, and the repo is private —
so "not published" means not on the course site, not confidential.)

## Reviews

| Date | File | Scope |
|---|---|---|
| 2026-09-09 | [`2026-09-09-content-review.md`](2026-09-09-content-review.md) | Notes and syllabus — 21 findings |

## Adding a review

Name the file `YYYY-MM-DD-<scope>.md` so reviews sort chronologically, add a row to
the table above, and record the commit reviewed — findings go stale as the content
changes, and a reader needs to know what was in front of you.

## Conventions

Findings are grouped by severity and given stable IDs, so they can be cited in
issues and commit messages without ambiguity:

| Prefix | Group | Meaning |
|---|---|---|
| `B` | Blocking | Wrong enough to mislead a student following the material |
| `C` | Correctness | Factually or internally inconsistent |
| `S` | Consistency | Contradictions between sections |
| `W` | Writing and structure | Clarity, accessibility, organization |
| — | Gaps | Not defects; material the content promises but does not cover |

Each finding states where it is, what is wrong, and what would resolve it.

**Reviews record; they do not apply.** Content decisions belong to whoever owns the
course material. The exception is a defect introduced by the same change that is
being reviewed — fix that, and mark it **[fixed]** in the finding so the record
stays honest about what was and was not changed.
