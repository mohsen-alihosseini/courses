# Study Courses

My course notes as reveal.js slide decks, built with [Quarto](https://quarto.org)
and published to GitHub Pages.

```
study-courses/
├── _quarto.yml                 site settings (title, navbar, theme)
├── index.qmd                   home page: lists every subject automatically
├── _macros.qmd                 shared LaTeX macros (\ket, \bra, ...)
├── theme/
│   ├── site.scss               look of the normal web pages
│   └── slides.scss             look of the slide decks
├── quantum/                    one folder per subject (category)
│   ├── index.qmd               subject page: lists its courses automatically
│   ├── thumbnail.svg           card image on the home page
│   └── basics-of-quantum-information/      one folder per course
│       ├── index.qmd           course page (title, description, lecture list)
│       ├── thumbnail.svg       card image on the subject page
│       ├── figures/            images used by the decks
│       └── lectures/
│           ├── _metadata.yml   makes every file here a reveal.js deck
│           ├── 01-single-systems.qmd
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

## Add a subject (category)

1. Make a folder at the top level, e.g. `math/`.
2. Copy `quantum/index.qmd` and `quantum/thumbnail.svg` into it, and change the
   `title`, `description` and `order` (position on the home page) and the
   intro text.

It appears on the home page on the next render. It shows "no matching items"
until it contains a course.

## Add a course

1. Copy an existing course folder, e.g. `quantum/basics-of-quantum-information/`,
   into the subject folder, e.g. `math/linear-algebra/`.
2. Edit its `index.qmd` (title, description, `order:`, the lecture table) and
   the `footer:` line in `lectures/_metadata.yml`. Change the back-link at the
   top of `index.qmd` to the subject's name.
3. Replace the decks in `lectures/` and the images in `figures/`. Each deck
   starts with a short YAML header (`title`, `subtitle`) and then
   `{{< include /_macros.qmd >}}`; every `##` heading is a new slide, every `#`
   heading a section divider.

Keep courses exactly two levels deep (`subject/course/`): the theme path in
`lectures/_metadata.yml` (`../../../theme/slides.scss`) assumes it.

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

The four quantum courses are adapted from *Basics of Quantum Information*,
*Fundamentals of Quantum Algorithms*, *General Formulation of Quantum
Information* and *Foundations of Quantum Error Correction* by John Watrous (© IBM Corp.), licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), and are
shared under the same license. The figures in each course's `figures/` folder
come from that course, except these new ones made by `scripts/make_figures.py`:
`grover-success.svg`, `query-counts.svg` and `basics-measure-classical.svg`.
