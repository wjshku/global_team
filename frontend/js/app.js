async function api(actionPayload) {
  const res = await fetch('/app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(actionPayload)
  });
  const data = await res.json();
  if (!res.ok || data.ok === false) {
    throw new Error(data.error || data.detail || 'Request failed');
  }
  return data;
}

function renderMembers(list) {
  const ul = document.getElementById('members');
  ul.innerHTML = '';
  for (const m of list) {
    const li = document.createElement('li');
    li.textContent = `${m.name} — ${m.timezone}`;
    ul.appendChild(li);
  }
}

async function refreshMembers() {
  try {
    const data = await api({ action: 'list_members' });
    renderMembers(data.members || []);
  } catch (e) {
    alert(e.message);
  }
}

document.getElementById('refresh').addEventListener('click', refreshMembers);

document.getElementById('add-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const timezone = document.getElementById('timezone').value.trim();
  if (!name || !timezone) return;
  try {
    await api({ action: 'add_member', name, timezone });
    document.getElementById('name').value = '';
    document.getElementById('timezone').value = '';
    await refreshMembers();
  } catch (e) {
    alert(e.message);
  }
});

document.getElementById('meeting-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const utc = document.getElementById('utc').value.trim();
  if (!utc) return;
  try {
    const data = await api({ action: 'propose_meeting', utc_datetime: utc });
    const container = document.getElementById('schedule');
    container.innerHTML = '';
    const p = document.createElement('p');
    p.textContent = `UTC: ${data.utc_datetime}`;
    container.appendChild(p);
    const table = document.createElement('table');
    table.innerHTML = '<thead><tr><th>Name</th><th>Timezone</th><th>Local</th><th>Weekday</th></tr></thead>';
    const tbody = document.createElement('tbody');
    for (const row of data.schedule || []) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${row.name}</td><td>${row.timezone}</td><td>${row.local_datetime || row.error || ''}</td><td>${row.weekday || ''}</td>`;
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    container.appendChild(table);
  } catch (e) {
    alert(e.message);
  }
});

// Teams: list & create
async function refreshTeams() {
  try {
    const data = await api({ action: 'list_teams' });
    const ul = document.getElementById('teams');
    ul.innerHTML = '';
    for (const t of data.teams || []) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `/app?team=${encodeURIComponent(t.name)}`;
      a.textContent = `${t.name} (${t.member_count})`;
      li.appendChild(a);
      ul.appendChild(li);
    }
  } catch (e) {
    console.error(e);
  }
}

document.getElementById('team-create-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('team-name').value.trim();
  if (!name) return;
  try {
    await api({ action: 'create_team', name });
    document.getElementById('team-name').value = '';
    await refreshTeams();
  } catch (e) {
    alert(e.message);
  }
});

// Team page logic with membership gate
async function enterTeam(team, requesterName) {
  const resp = await api({ action: 'get_team', team, requester_name: requesterName });
  const list = document.getElementById('team-members');
  list.innerHTML = '';
  for (const m of resp.members || []) {
    const li = document.createElement('li');
    li.textContent = `${m.name} — ${m.timezone || ''}`;
    list.appendChild(li);
  }
  document.getElementById('team-content').hidden = false;
}

function showHome() {
  document.getElementById('view-home').hidden = false;
  document.getElementById('view-team').hidden = true;
  document.getElementById('nav-team').textContent = '';
  refreshMembers();
  refreshTeams();
}

function showTeam(team) {
  document.getElementById('view-home').hidden = true;
  document.getElementById('view-team').hidden = false;
  document.getElementById('team-title').textContent = `Team: ${team}`;
  const navTeam = document.getElementById('nav-team');
  navTeam.innerHTML = ` / <strong>${team}</strong>`;
  // Gate via form
  const authForm = document.getElementById('team-auth-form');
  authForm.onsubmit = async (e) => {
    e.preventDefault();
    const requester = document.getElementById('requester-name').value.trim();
    if (!requester) return;
    try {
      await enterTeam(team, requester);
    } catch (err) {
      alert(err.message);
    }
  };
  // Add member to team
  const addForm = document.getElementById('team-add-member-form');
  addForm.onsubmit = async (e) => {
    e.preventDefault();
    const memberName = document.getElementById('team-member-name').value.trim();
    if (!memberName) return;
    try {
      await api({ action: 'add_member_to_team', team, member_name: memberName });
      document.getElementById('team-member-name').value = '';
      const requester = document.getElementById('requester-name').value.trim();
      if (requester) {
        await enterTeam(team, requester);
      }
    } catch (e) {
      alert(e.message);
    }
  };
}

// Simple routing using query param
function initRouter() {
  const url = new URL(window.location.href);
  const team = url.searchParams.get('team');
  if (team) {
    showTeam(team);
  } else {
    showHome();
  }
}

initRouter();


