# Study Courses

My course notes as reveal.js slide decks, built with [Quarto](https://quarto.org)
and published to GitHub Pages.

```
study-courses/
├── _quarto.yml                 site settings (title, navbar, theme)
├── index.qmd                   home page: lists every course automatically
├── _macros.qmd                 shared LaTeX macros (\ket, \bra, ...)
├── theme/
│   ├── site.scss               look of the normal web pages
│   └── slides.scss             look of the slide decks
├── courses/
│   └── fundamentals-of-quantum-algorithms/
│       ├── index.qmd           course page (title, description, lecture list)
│       ├── thumbnail.svg       card image on the home page
│       ├── figures/            images used by the decks
│       └── lectures/
│           ├── _metadata.yml   makes every file here a reveal.js deck
│           ├── 01-quantum-query-algorithms.qmd
│           └── ...
└── .github/workflows/publish.yml   builds and publishes on every push
```

## Work on it locally

1. Install Quarto: <https://quarto.org/docs/get-started/>
2. In this folder run `quarto preview`. A browser opens and reloads every time
   you save a file.

No Python or R is needed: the decks contain no executed code. The interactive
demos are Observable JS cells, which run in the browser.

## Publish on GitHub Pages

1. Create a repository on GitHub (for example `study-courses`) and push this
   folder to its `main` branch.
2. In the repository: **Settings → Pages → Build and deployment → Source:
   GitHub Actions**.
3. Every push to `main` now rebuilds the site. It appears at
   `https://<your-username>.github.io/study-courses/`.
4. Replace `YOUR-USERNAME` in `_quarto.yml` with your GitHub username.

## Add a course

1. Copy `courses/fundamentals-of-quantum-algorithms/` to
   `courses/<new-course>/`.
2. Edit `index.qmd` there (title, description, `order:`, the lecture table)
   and the `footer:` line in `lectures/_metadata.yml`.
3. Replace the decks in `lectures/`. Each deck starts with a short YAML header
   (`title`, `subtitle`) and then `{{< include /_macros.qmd >}}`; every
   `##` heading is a new slide, every `#` heading a section divider.

The home page picks the new course up on the next render.

## Slide syntax cheat sheet

| You write | You get |
|---|---|
| `## Title` | a new slide |
| `# Part` | a section divider slide |
| `::: {.box}` … `:::` | a boxed definition / problem statement |
| `:::: {.columns}` `::: {.column width="50%"}` | side-by-side columns |
| `::: {.notes}` … `:::` | speaker notes (press **S**) |
| `. . .` on its own line | pause: the rest appears on the next click |
| `## Title {.scrollable}` | a slide that scrolls if it is long |

## License

The two quantum courses are adapted from *Basics of Quantum Information* and
*Fundamentals of Quantum Algorithms* by John Watrous (© IBM Corp.), licensed
under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), and are
shared under the same license. The figures in each course's `figures/` folder
come from that course, except these new ones made by `scripts/make_figures.py`:
`grover-success.svg`, `query-counts.svg` and `basics-measure-classical.svg`.
