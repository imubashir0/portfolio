"""Render the portfolio's static HTML. Requires only Python 3.9+."""
import argparse
import json
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urljoin

from icons import icon

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
RESUME = "assets/files/Mubashir_Ishimwe_IT_Analyst_Nov26.pdf"
PUBLIC_URL = "https://imubashir0.github.io/portfolio/"
DESCRIPTION = "Mubashir Ishimwe’s Ottawa IT portfolio. Explore Windows support, networking labs, custom PC builds, and hands-on deployment work."
HERO_ALT = "An illustrated vintage computer with a green wireframe landscape beside a network switch."
SKILLS = [
    ("support", "Service desk", "Salesforce CRM, IT ticketing, user guidance, incident documentation, ITIL fundamentals, print and conferencing support."),
    ("network", "Identity & systems", "Active Directory, Group Policy, Microsoft Entra ID, Exchange, Windows Server, Linux, DFS, Microsoft 365, and Google Workspace."),
    ("wifi", "Networking", "TCP/IP, DNS, DHCP, VPN, SSH, Wi-Fi, access control lists, Layer 3 switching, and Cisco and Aruba fundamentals."),
    ("cpu", "Hardware & deployment", "PC assembly, hardware repair, Windows imaging, Windows ADK, WinPE, drivers, updates, and asset tracking."),
    ("layers", "Virtualization & recovery", "VMware ESXi, Docker, Proxmox backup planning, Veeam, RAID, ZFS, retention policies, and lab restore testing."),
    ("code", "Scripting & data", "Python and Bash scripting, SQL queries, and using logs to investigate and document system behaviour."),
]


def template(template_name, **values):
    source = (SOURCE / "templates" / (template_name + ".html")).read_text(encoding="utf-8")
    return Template(source).substitute(values)


def tags(values):
    return "".join(f'<span class="tag">{escape(value)}</span>' for value in values)


def cover_image(project, root="", size="card"):
    name = project["cover"]
    path = root + "assets/images/" + name
    sizes = "(max-width: 520px) 93vw, (max-width: 720px) 42vw, 31vw" if size == "card" else "92vw"
    return (f'<img src="{path}.webp" srcset="{path}-small.webp 650w, {path}.webp 1250w" '
            f'sizes="{sizes}" width="1250" height="833" loading="lazy" decoding="async" '
            f'alt="{escape(project["coverAlt"])}">')


def featured_card(project):
    slug = project["slug"]
    return f"""
          <a class="feature-card {project['cover']}-tone" href="projects/{slug}.html" aria-labelledby="feature-{slug}">
            <div class="cover">{cover_image(project)}</div>
            <div class="card-body">
              <p class="card-category">{icon(project['icon'])}{escape(project['discipline'])}</p>
              <h3 id="feature-{slug}">{escape(project['name'])}</h3>
              <p>{escape(project['summary'])}</p>
              <div class="tag-list">{tags(project['tools'][:2])}</div>
            </div>
          </a>"""


def skill_item(glyph, title, text):
    return f"""
          <div class="skill-item">
            <div class="skill-heading"><span class="skill-symbol">{icon(glyph)}</span><h3>{escape(title)}</h3></div>
            <p>{escape(text)}</p>
          </div>"""


def archive_row(project):
    p = project
    slug = p["slug"]
    theme = "type-" + p["category"].lower()
    words = " ".join([p["name"], p["summary"], p["discipline"], p["category"], p["setting"],
                      p["role"], p["date"], *p["tools"], *p["platforms"]])
    fields = {"slug": slug, "name": p["name"], "category": p["category"], "date": p["date"],
              "setting": p["setting"], "platforms": "|".join(p["platforms"]), "level": p["level"] or "",
              "tools": ", ".join(p["tools"]), "result": p["result"], "search": words}
    attributes = " ".join(f'data-{key}="{escape(value, quote=True)}"' for key, value in fields.items())
    return f"""
          <a class="archive-row" {attributes} href="{slug}.html" aria-labelledby="row-{slug}">
            <span class="type-symbol {theme}">{icon(p['icon'])}</span>
            <div><span class="archive-discipline {theme}">{escape(p['discipline'])}</span>
              <h2 id="row-{slug}">{escape(p['name'])}</h2><p>{escape(p['summary'])}</p></div>
            <span class="archive-date">{escape(p['date'])}</span>
          </a>"""


def render_page(output, path, body, title, description, base_url, page_class, project=None):
    is_home = path == "index.html"
    root = "" if is_home else "../"
    resume_url = root + RESUME
    is_archive = path == "projects/index.html"
    header = template("header", home_link="#top" if is_home else root + "index.html",
                      home_anchor="" if is_home else root + "index.html",
                      projects_link="#projects" if is_home else "index.html",
                      project_current="" if is_home else (' aria-current="page"' if is_archive else ' aria-current="location"'),
                      resume_url=resume_url, terminal_icon=icon("terminal"), file_icon=icon("file"),
                      menu_icon=icon("menu", "menu-icon"), close_icon=icon("close", "close-icon"))
    footer = template("footer", resume_url=resume_url, file_icon=icon("file"), email_icon=icon("mail"),
                      github_icon=icon("github"), linkedin_icon=icon("linkedin"), pin_icon=icon("pin"))
    canonical = urljoin(base_url, path.removesuffix("index.html"))
    image_name = project.get("cover", "hero") if project else "hero"
    image_alt = project.get("coverAlt", HERO_ALT) if project else HERO_ALT
    html = template("base", root=root, header=header, footer=footer, content=body, page_class=page_class,
                    title=escape(title), description=escape(description), canonical=escape(canonical),
                    social_image=escape(urljoin(base_url, f"assets/images/{image_name}-share.jpg")), social_alt=escape(image_alt))
    destination = output / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html + "\n", encoding="utf-8")


def detail_body(project, projects):
    p = project
    steps = "\n".join(f"<li><h3>{escape(title)}</h3><p>{escape(text)}</p></li>" for title, text in p["steps"])
    visual = ""
    if "cover" in p:
        visual = (f'<figure class="case-visual">{cover_image(p, "../", "detail")}'
                  f'<figcaption>Editorial illustration · {escape(p["discipline"])}</figcaption></figure>')
    related = ""
    if p.get("related"):
        other = next(item for item in projects if item["slug"] == p["related"])
        related = (f'<div class="related-case"><a class="text-link on-light" href="{other["slug"]}.html">'
                   f'{icon("book")} Related case study · {escape(other["name"])}</a></div>')
    return template("project", discipline=escape(p["discipline"]), name=escape(p["name"]), summary=escape(p["summary"]),
                    date=escape(p["date"]), setting=escape(p["setting"]), role=escape(p["role"]), purpose=escape(p["purpose"]),
                    result_label=escape(p["resultLabel"]), result=escape(p["result"]), takeaway=escape(p["takeaway"]),
                    steps=steps, visual=visual, tool_tags=tags(p["tools"]), related=related, grid_icon=icon("folder-grid"),
                    book_icon=icon("book"), project_count=len(projects))


def archive_body(projects):
    categories = [""] + sorted({p["category"] for p in projects})
    platforms = sorted({platform for p in projects for platform in p["platforms"]})
    buttons = [f'<button type="button" class="category-button" data-category="{escape(c)}" '
               f'aria-pressed="{str(not c).lower()}">{escape(c) if c else "All projects"}</button>' for c in categories]
    options = [f'<option value="{p["slug"]}">{escape(p["name"])}</option>' for p in projects]
    return template("archive", project_count=len(projects), category_buttons="\n".join(buttons),
                    platform_options="".join(f"<option>{escape(p)}</option>" for p in platforms),
                    compare_options="".join(options), archive_rows="".join(archive_row(p) for p in projects),
                    search_icon=icon("search"), sliders_icon=icon("sliders"), compare_icon=icon("compare"))


def build(output, base_url):
    projects = json.loads((SOURCE / "projects.json").read_text(encoding="utf-8"))
    featured = [p for p in projects if p.get("cover")]
    home = template("home", project_count=len(projects), featured_cards="".join(featured_card(p) for p in featured),
                    skill_cards="".join(skill_item(*s) for s in SKILLS), folder_icon=icon("folder"), email_icon=icon("mail"),
                    file_icon=icon("file"), pin_icon=icon("pin"), education_icon=icon("graduation"),
                    grid_icon=icon("folder-grid"), book_icon=icon("book"), support_icon=icon("support"), resume_url=RESUME)
    render_page(output, "index.html", home, "Mubashir Ishimwe | IT Support & Networking", DESCRIPTION, base_url, "home-page")
    render_page(output, "projects/index.html", archive_body(projects), "Project archive | Mubashir Ishimwe",
                "Browse and compare Mubashir Ishimwe’s systems, infrastructure, hardware, and networking projects.",
                base_url, "archive-page")
    for project in projects:
        render_page(output, f'projects/{project["slug"]}.html', detail_body(project, projects),
                    project["name"] + " | Mubashir Ishimwe", project["summary"], base_url, "detail-page", project)
    (output / "404.html").write_text(template("notfound", base_url=escape(base_url), terminal_icon=icon("terminal")) + "\n",
                                     encoding="utf-8")
    print(f"Rendered the homepage, the archive, {len(projects)} case studies, and the 404 page.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT, help="directory containing the public assets folder")
    parser.add_argument("--base-url", default=PUBLIC_URL, help="full public URL including the repository subpath")
    args = parser.parse_args()
    build(args.output.resolve(), args.base_url.rstrip("/") + "/")

