# Mubashir Ishimwe | IT portfolio

A static GitHub Pages portfolio with nine project case studies, professional experience, a technical skills section, and the November 2026 résumé. The homepage, individual project pages, and résumé link work with JavaScript disabled. JavaScript adds archive search, filtering, project comparison, and the compact mobile navigation.

## Publish on GitHub Pages

1. Extract the contents of the ZIP into the root of the `portfolio` repository. Keep `index.html`, `assets/`, `projects/`, and `.nojekyll` at the same level.
2. Commit the new files to the branch used for GitHub Pages.
3. In **Settings → Pages → Build and deployment**, select **Deploy from a branch** and choose that branch and **/(root)** if branch publishing is not already configured.

The pages are ready to publish directly. The default public address for the export is <https://imubashir0.github.io/portfolio/>. [GitHub Pages publishing settings](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Preview

From the extracted repository, run `python -m http.server 8000` and open <http://localhost:8000/>. Run `python3` in place of `python` if that is how your system exposes Python.

## Update the portfolio

| Content | Source |
| --- | --- |
| Project tiles, archive, and case studies | `source/projects.json` |
| Homepage text, roles, and education | `source/templates/home.html` |
| Skills and résumé filename | `source/build.py` |
| Navigation and contact links | `source/templates/header.html` and `source/templates/footer.html` |
| Site styling and interactions | `assets/css/styles.css` and `assets/js/site.js` |
| Downloadable PDF | `assets/files/Mubashir_Ishimwe_IT_Analyst_Nov26.pdf` |

After editing the content or templates, run `python source/build.py` from the repository. It regenerates the HTML with Python 3.9 or later and the standard library. For a different domain or repository name, pass its full address with `--base-url`. This updates social previews, canonical URLs, and the 404 return link.

The supplied portrait is from the previous portfolio. The computer and hardware cover images are editorial illustrations. Inter is self-hosted under the SIL Open Font License in `assets/fonts/OFL-Inter.txt`.

