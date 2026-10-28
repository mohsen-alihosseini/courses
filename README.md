# Study Courses
**live view on** : [https://mohsen-alihosseini.github.io/courses/](https://mohsen-alihosseini.github.io/courses/)

My course notes as reveal.js slide decks, built with [Quarto](https://quarto.org)
and published to GitHub Pages.

## Site map

The site has three levels: **home page → subject → course**. Each course page
lists its lecture decks.

```
Home (index.qmd)
├── Quantum (quantum/)
│   ├── Basics of Quantum Information ............ 4 decks
│   ├── Fundamentals of Quantum Algorithms ....... 4 decks
│   ├── General Formulation of Quantum Information 4 decks
│   └── Foundations of Quantum Error Correction .. 4 decks
└── Math (math/)
    └── Mathematics for Machine Learning ......... chapters 2–7 (Part I)
```

## Folder structure

```
study-courses/
├── _quarto.yml                 site settings (title, navbar, theme)
├── index.qmd                   home page: one card per subject
├── _macros.qmd                 shared LaTeX macros (\ket, \R, \rk, ...)
├── theme/
│   ├── site.scss               look of the normal web pages
│   └── slides.scss             look of the slide decks
├── scripts/
│   └── make_figures.py         regenerates the figures made for this site
├── quantum/                    subject: Quantum
│   ├── index.qmd               subject page: lists its courses automatically
│   ├── thumbnail.svg           card image on the home page
│   ├── basics-of-quantum-information/
│   │   ├── index.qmd           course page (description, lecture table)
│   │   ├── thumbnail.svg       card image on the subject page
│   │   ├── figures/            images used by the decks
│   │   └── lectures/
│   │       ├── _metadata.yml   makes every file here a reveal.js deck
│   │       ├── 01-single-systems.qmd
│   │       ├── 02-multiple-systems.qmd
│   │       ├── 03-quantum-circuits.qmd
│   │       └── 04-entanglement-in-action.qmd
│   ├── fundamentals-of-quantum-algorithms/
│   │   └── lectures/           01-quantum-query-algorithms … 04-grover-algorithm
│   ├── general-formulation-of-quantum-information/
│   │   └── lectures/           01-density-matrices … 04-purifications-and-fidelity
│   └── foundations-of-quantum-error-correction/
│       └── lectures/           01-correcting-quantum-errors … 04-fault-tolerant-quantum-computing
├── math/                       subject: Math
│   ├── index.qmd
│   ├── thumbnail.svg
│   └── mathematics-for-machine-learning/
│       ├── index.qmd           lists all 12 book chapters; written ones are linked
│       ├── book_cover.jpg      the book's cover
│       ├── cover-card.jpg      card image made from it (wide format)
│       ├── figures/
│       └── lectures/
│           ├── _metadata.yml
│           ├── 02-linear-algebra.qmd
│           ├── 03-analytic-geometry.qmd
│           ├── 04-matrix-decompositions.qmd
│           ├── 05-vector-calculus.qmd
│           ├── 06-probability-and-distributions.qmd
│           └── 07-continuous-optimization.qmd
└── .github/workflows/publish.yml   builds and publishes on every push
```

Every course folder has the same four parts (`index.qmd`, `thumbnail.svg`,
`figures/`, `lectures/`); only the first one is shown in full above.

## Work on it locally

1. Install Quarto: <https://quarto.org/docs/get-started/>
2. In this folder run `quarto preview`. A browser opens and reloads every time
   you save a file.

No Python or R is needed to build the site: the decks contain no executed
code. The interactive demos are Observable JS cells, which run in the browser.
Python with NumPy and Matplotlib is only needed to rerun
`scripts/make_figures.py`.

## Publish

The repository is
[mohsen-alihosseini/courses](https://github.com/mohsen-alihosseini/courses),
and GitHub Pages is set to **Source: GitHub Actions**. Every push to `master`
(or `main`) rebuilds and publishes the site:

```
git add -A
git commit -m "Describe the change"
git push
```

The build takes a few minutes; watch it in the repository's **Actions** tab.
It can also be started by hand there: **Publish site → Run workflow**.

## Add a subject (category)

1. Make a folder at the top level, e.g. `ml/`.
2. Copy `math/index.qmd` and `math/thumbnail.svg` into it, and change the
   `title`, `description` and `order` and the intro text.
3. In the top-level `index.qmd`, copy one `<a class="subject-card"> ... </a>`
   block, paste it after the last one, and change the folder name
   (`ml/index.html`, `ml/thumbnail.svg`), title, description and course count.

Courses inside a subject folder appear on that subject's page automatically.

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
4. Update the course count on the subject's card in the top-level `index.qmd`.

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

## License and sources

**Quantum** (`quantum/`): the four courses are adapted from *Basics of Quantum
Information*, *Fundamentals of Quantum Algorithms*, *General Formulation of
Quantum Information* and *Foundations of Quantum Error Correction* by John
Watrous (© IBM Corp.), from
[Qiskit/documentation](https://github.com/Qiskit/documentation), licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). These slides
are shared under the same license. The figures in their `figures/` folders come
from those courses, except `grover-success.svg`, `query-counts.svg` and
`basics-measure-classical.svg`, which are made by `scripts/make_figures.py`.
This site is not affiliated with or endorsed by IBM.

**Math** (`math/`): the slides follow the chapter structure of *Mathematics for
Machine Learning* by M. P. Deisenroth, A. A. Faisal and C. S. Ong (Cambridge
University Press, 2020; free to read at
[mml-book.github.io](https://mml-book.github.io/)). The book's PDF is licensed
for personal use only, so no text, figures, examples or exercises from it are
reproduced here: all explanations, examples and figures are original. The
cover image (`book_cover.jpg`, `cover-card.jpg`) is © Cambridge University
Press and is shown only to identify the book.
