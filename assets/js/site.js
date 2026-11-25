"use strict";

function setupNavigation() {
  const menu = document.querySelector(".menu-button");
  const nav = document.getElementById("site-navigation");
  const compact = window.matchMedia("(max-width: 720px)");

  function setOpen(open) {
    nav.classList.toggle("is-open", open);
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  }

  function updateMenu() {
    menu.hidden = !compact.matches;
    setOpen(false);
  }

  document.body.classList.add("menu-ready");
  updateMenu();
  compact.addEventListener("change", updateMenu);
  menu.addEventListener("click", () => setOpen(menu.getAttribute("aria-expanded") !== "true"));
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) setOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      menu.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header") && nav.classList.contains("is-open")) setOpen(false);
  });

  if (!document.body.classList.contains("home-page") || !("IntersectionObserver" in window)) return;
  const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
  const sections = links.map((link) => document.querySelector(link.hash));
  const visible = new Set();
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) visible.add(entry.target);
      else visible.delete(entry.target);
    }
    const active = sections.find((section) => visible.has(section));
    for (const link of links) {
      if (active && link.hash === "#" + active.id) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }, {rootMargin: "-12% 0px -52% 0px"});
  for (const section of sections) if (section) observer.observe(section);
}

function searchable(value) {
  return value.normalize("NFKD").toLowerCase().replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

function setupArchive(rows) {
  const tools = document.getElementById("archive-tools");
  const search = document.getElementById("project-search");
  const platform = document.getElementById("platform-filter");
  const difficulty = document.getElementById("difficulty-filter");
  const filterToggle = document.getElementById("filter-toggle");
  const filterPanel = document.getElementById("filter-panel");
  const filterCount = document.getElementById("filter-count");
  const resultCount = document.getElementById("result-count");
  const empty = document.getElementById("empty-state");
  const categories = Array.from(document.querySelectorAll(".category-button"));
  const index = rows.map((row) => ({
    row,
    words: searchable(row.dataset.search),
    platforms: row.dataset.platforms.split("|")
  }));
  const params = new URLSearchParams(location.search);
  search.value = params.get("q") || "";
  platform.value = params.get("platform") || "";
  difficulty.value = params.get("level") || "";
  let category = categories.some((item) => item.dataset.category === params.get("category"))
    ? params.get("category") : "";

  function saveQuery() {
    if (!["http:", "https:"].includes(location.protocol)) return;
    const url = new URL(location.href);
    const values = {q: search.value.trim(), category, platform: platform.value, level: difficulty.value};
    for (const [key, value] of Object.entries(values)) {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    }
    if (url.href !== location.href) history.replaceState(history.state, "", url);
  }

  function filter(save = true) {
    const terms = searchable(search.value).split(" ").filter(Boolean);
    let count = 0;
    for (const {row, words, platforms} of index) {
      const matches = (!category || row.dataset.category === category)
        && (!platform.value || platforms.includes(platform.value))
        && (!difficulty.value || row.dataset.level === difficulty.value)
        && terms.every((term) => words.includes(term));
      row.hidden = !matches;
      if (matches) count += 1;
    }
    for (const button of categories) {
      button.setAttribute("aria-pressed", String(button.dataset.category === category));
    }
    const active = Number(Boolean(platform.value)) + Number(Boolean(difficulty.value));
    filterCount.hidden = active === 0;
    filterCount.textContent = active ? "(" + active + ")" : "";
    resultCount.textContent = count + (count === 1 ? " project" : " projects");
    empty.hidden = count > 0;
    if (save) saveQuery();
  }

  function showPanel(open) {
    filterPanel.hidden = !open;
    filterToggle.setAttribute("aria-expanded", String(open));
  }

  filterToggle.addEventListener("click", () => showPanel(filterPanel.hidden));
  for (const button of categories) {
    button.addEventListener("click", () => { category = button.dataset.category; filter(); });
  }
  search.addEventListener("input", () => filter());
  platform.addEventListener("change", () => filter());
  difficulty.addEventListener("change", () => filter());
  for (const button of document.querySelectorAll(".reset-filters")) {
    button.addEventListener("click", () => {
      search.value = "";
      category = "";
      platform.value = "";
      difficulty.value = "";
      filter();
      search.focus();
    });
  }
  tools.hidden = false;
  showPanel(Boolean(platform.value || difficulty.value));
  filter(false);
}

function setupComparison(rows) {
  const toggle = document.getElementById("compare-start");
  const panel = document.getElementById("compare-panel");
  const output = document.getElementById("comparison");
  const a = document.getElementById("compare-a");
  const b = document.getElementById("compare-b");
  const projects = new Map(rows.map((row) => [row.dataset.slug, row]));
  const fields = [["Timeframe", "date"], ["Setting", "setting"], ["Tools", "tools"], ["Outcome", "result"]];

  function renderComparison() {
    for (const option of a.options) option.disabled = Boolean(option.value && option.value === b.value);
    for (const option of b.options) option.disabled = Boolean(option.value && option.value === a.value);
    output.replaceChildren();
    const selected = [projects.get(a.value), projects.get(b.value)];
    if (!selected[0] || !selected[1] || selected[0] === selected[1]) return;

    const table = document.createElement("table");
    table.className = "compare-table";
    const caption = table.createCaption();
    caption.textContent = "Selected projects side by side";
    caption.className = "sr-only";
    const heading = table.createTHead().insertRow();
    const first = document.createElement("th");
    first.scope = "col";
    first.textContent = "Project";
    heading.append(first);
    for (const project of selected) {
      const th = document.createElement("th");
      const link = document.createElement("a");
      link.href = project.getAttribute("href");
      link.textContent = project.dataset.name;
      th.scope = "col";
      th.append(link);
      heading.append(th);
    }
    const body = table.createTBody();
    for (const [label, key] of fields) {
      const row = body.insertRow();
      const th = document.createElement("th");
      th.scope = "row";
      th.textContent = label;
      row.append(th);
      for (const project of selected) row.insertCell().textContent = project.dataset[key];
    }
    output.append(table);
  }

  toggle.hidden = false;
  toggle.addEventListener("click", () => {
    panel.hidden = !panel.hidden;
    toggle.setAttribute("aria-expanded", String(!panel.hidden));
    if (!panel.hidden) a.focus();
  });
  a.addEventListener("change", renderComparison);
  b.addEventListener("change", renderComparison);
}

setupNavigation();
const projectRows = Array.from(document.querySelectorAll(".archive-row"));
if (projectRows.length) {
  setupArchive(projectRows);
  setupComparison(projectRows);
}

