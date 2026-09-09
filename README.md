# Artificial Intelligence

Course notes and materials, built as a [Quarto](https://quarto.org) website and published to GitHub Pages.

The notes follow one running example: a two-wheel autonomous robot that avoids obstacles using a small INT8-quantized neural network running on an STM32 microcontroller.

## Layout

```
pixi.toml / pixi.lock                    pinned toolchain (Quarto)
_quarto.yml                              site config (nav, sidebar, theme)
index.qmd                                landing page
notes/
  01-ai-model.qmd                        the network and the environment
  02-agent-and-environment.qmd           sensors → inference → motor commands
  03-formal-model.qmd                    states, actions, transitions
docs/syllabus/
  index.md                               course syllabus
docs/reviews/                            editorial reviews (not published)
images/                                  figures
.github/workflows/publish.yml            render + deploy to GitHub Pages
```

`_site/` (rendered output) and `.pixi/` (the environment) are git-ignored.

`docs/reviews/` is excluded from the rendered site — it holds editorial notes on the
course content, which are tracked in the repo but not published to students.

## Working locally

The only prerequisite is [pixi](https://pixi.sh) — it installs Quarto itself, pinned by `pixi.lock`, so nothing needs to be installed globally.

```bash
pixi run preview     # live-reloading local preview
pixi run render      # build into _site/
pixi run check       # verify the Quarto installation
```

The first command bootstraps the environment automatically. There are no executable code cells, so no R or Python runtime is required.

## Publishing

Pushing to `main` renders the site with the same pinned toolchain and deploys it via GitHub Actions.

One-time setup: in **Settings → Pages**, set **Source** to **GitHub Actions**.
