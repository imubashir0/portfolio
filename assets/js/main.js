(function(){
  'use strict';
  const $ = (sel, ctx=document) => ctx.querySelector(sel);
  const $$ = (sel, ctx=document) => Array.from(ctx.querySelectorAll(sel));

  // Build project cards
  const grid = $('#project-grid');
  const compareBar = $('#compare');
  const leftTile = $('#compare-left');
  const rightTile = $('#compare-right');
  const caseModal = $('#case-modal');
  const caseTitle = $('#case-title');
  const caseBody = $('#case-body');
  const caseClose = $('#case-close');
  const chosen = new Set();

  function renderProjects() {
    if (!window.__PROJECTS__) return;
    const q = ($('#search')?.value || '').toLowerCase();
    const os = $('#os-filter')?.value || 'All';
    const diff = $('#diff-filter')?.value || 'All';

    grid.innerHTML = '';
    window.__PROJECTS__.forEach(p => {
      if (os !== 'All' && !(p.os||[]).includes(os)) return;
      if (diff !== 'All' && p.difficulty !== diff) return;
      const blob = JSON.stringify(p).toLowerCase();
      if (q && !blob.includes(q)) return;

      const card = document.createElement('article');
      card.className = 'card';
      card.innerHTML = `
        <div class="content">
          <h3>${p.title}</h3>
          <p class="muted">${p.when}</p>
          <div class="taglist">${p.stack.map(s=>`<span class="tag">${s}</span>`).join('')}</div>
          <p>${p.impact}</p>
          <div style="display:flex; gap:.5rem; margin-top:.5rem;">
            <button class="btn" data-id="${p.id}" data-action="case">Details</button>
            <label style="display:flex; align-items:center; gap:.35rem;font-size:.95rem;">
              <input type="checkbox" data-id="${p.id}" data-action="compare"> Compare
            </label>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  function projectById(id){ return window.__PROJECTS__.find(p=>p.id===id); }

  function updateCompareBar(){
    const arr = Array.from(chosen);
    if (arr.length) compareBar.classList.add('active'); else compareBar.classList.remove('active');
    const [a, b] = [projectById(arr[0]), projectById(arr[1])];
    leftTile.innerHTML = a ? renderTile(a) : '<em>Select first project</em>';
    rightTile.innerHTML = b ? renderTile(b) : '<em>Select second project</em>';
  }

  function renderTile(p){
    return `
      <strong>${p.title}</strong><br>
      <small>${p.when}</small>
      <div class="taglist" style="margin:.4rem 0;">${p.stack.map(s=>`<span class="tag">${s}</span>`).join('')}</div>
      <div style="font-size:.95rem;">
        <div>Difficulty: <b>${p.difficulty}</b></div>
        <div>Role: <b>${p.role}</b></div>
        <div>Outcome: ${p.outcome}</div>
      </div>
    `;
  }

  function renderCase(p){
    caseTitle.textContent = p.title;
    caseBody.innerHTML = `
      <p><b>Problem</b>: ${p.problem}</p>
      <p><b>Approach</b>: ${p.approach}</p>
      <p><b>Impact</b>: ${p.impact}</p>
      <p><b>Outcome</b>: ${p.outcome}</p>
      <p><b>Lessons</b>: ${p.lessons}</p>
      <p class="muted"><small>${p.when} — ${p.role}</small></p>
    `;
    caseModal.showModal();
  }

  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const id = btn.dataset.id;
    const p = projectById(id);
    if (btn.dataset.action === 'case') {
      renderCase(p);
    }
  });

  document.addEventListener('change', (e)=>{
    const cb = e.target.closest('input[type="checkbox"][data-action="compare"]');
    if (!cb) return;
    const id = cb.dataset.id;
    if (cb.checked) {
      if (chosen.size >= 2) {
        const first = chosen.values().next().value;
        chosen.delete(first);
      }
      chosen.add(id);
    } else {
      chosen.delete(id);
    }
    updateCompareBar();
  });

  ['search','os-filter','diff-filter'].forEach(id=>{
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', renderProjects);
  });

  if (caseClose) caseClose.addEventListener('click', ()=>caseModal.close());

  renderProjects();

  $$('a[data-prefetch]').forEach(a=>{
    a.addEventListener('mouseover', ()=>{
      const href = a.getAttribute('href'); if (!href) return;
      const link = document.createElement('link'); link.rel='prefetch'; link.href=href; document.head.appendChild(link);
    }, {once:true});
  });
})();