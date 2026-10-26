// The demo on the top page: the right edge of a small Mac desktop. Rest on it, choose a
// friend, bump it three times; they answer and a room opens. Nothing leaves the browser.
(() => {
  const text = JSON.parse(document.getElementById('demoText').textContent);
  const $ = (id) => document.getElementById(id);
  const desk = $('desk'), edge = $('edge'), dial = $('dial'), status = $('status');
  const room = $('room'), tiles = $('tiles'), bubbles = $('bubbles'), lightbox = $('lightbox');
  const colors = ['var(--haru)', 'var(--nagi)', 'var(--ao)'];
  const state = { phase: 'idle', selected: 0, bumps: [], timers: [] };

  const say = (key, name) => { status.textContent = text[key].replace('{name}', name ?? ''); };
  const later = (fn, ms) => state.timers.push(setTimeout(fn, ms));
  const clearTimers = () => { state.timers.forEach(clearTimeout); state.timers = []; };
  const setPhase = (phase) => { state.phase = phase; desk.dataset.phase = phase; };
  const person = () => text.people[state.selected];

  // The dial: the friends along the edge, the chosen one in the middle and named.
  text.people.forEach((name, i) => {
    const el = document.createElement('div');
    el.className = 'person';
    el.style.background = colors[i];
    el.innerHTML = `${name[0]}<span class="name">${name}</span>`;
    dial.appendChild(el);
  });
  const drawDial = () => {
    [...dial.children].forEach((el, i) => {
      const offset = i - state.selected;
      el.classList.toggle('on', offset === 0);
      el.style.top = `${150 + offset * 62}px`;
    });
  };
  drawDial();

  const drawBumps = () => {
    [...$('bumps').children].forEach((el, i) => el.classList.toggle('hit', i < state.bumps.length));
  };

  const rest = () => {
    if (state.phase !== 'idle') return;
    clearTimers();
    state.bumps = [];
    drawBumps();
    setPhase('edge');
    say('edge');
  };

  const leave = () => {
    if (state.phase !== 'edge') return;
    later(() => { if (state.phase === 'edge' && !edge.matches(':hover')) { setPhase('idle'); say('idle'); } }, 1400);
  };

  // A bump: the cursor pushed out past the edge (or a click / Enter on it). Three within
  // two seconds knock.
  const bump = () => {
    if (state.phase === 'idle') rest();
    if (state.phase !== 'edge') return;
    const now = performance.now();
    state.bumps = state.bumps.filter((t) => now - t < 2000).concat(now);
    drawBumps();
    desk.classList.remove('shake');
    void desk.offsetWidth;
    desk.classList.add('shake');
    if (state.bumps.length >= 3) knock();
  };

  const knock = () => {
    clearTimers();
    setPhase('knocking');
    say('knocking', person());
    later(openRoom, 1700);
  };

  const openRoom = () => {
    const i = state.selected;
    $('roomName').textContent = person();
    const avatar = $('roomAvatar');
    avatar.textContent = person()[0];
    avatar.style.background = colors[i];
    $('theirLabel').textContent = person();
    $('theirCursor').querySelector('svg').style.fill = colors[i];
    $('theirLabel').style.background = colors[i];
    tiles.innerHTML = '';
    bubbles.innerHTML = '';
    $('showMe').disabled = false;
    setPhase('room');
    say('room', person());
    wander();
  };

  const wander = () => {
    if (state.phase !== 'room') return;
    const cursor = $('theirCursor');
    cursor.style.left = `${10 + Math.random() * 65}%`;
    cursor.style.top = `${15 + Math.random() * 55}%`;
    later(wander, 1600 + Math.random() * 900);
  };

  const bubble = (words, theirs) => {
    const el = document.createElement('div');
    el.className = theirs ? 'bubble them' : 'bubble';
    el.textContent = words;
    bubbles.appendChild(el);
    while (bubbles.children.length > 3) bubbles.firstChild.remove();
  };

  text.replies.forEach((words, i) => {
    const b = document.createElement('button');
    b.textContent = words;
    b.addEventListener('click', () => {
      bubble(words, false);
      later(() => bubble(text.theirReplies[i], true), 900);
    });
    $('replies').appendChild(b);
  });

  const miniScreen = () => `<div class="mini"><div class="side"></div><div class="main"><div class="bar"></div><div class="cards"><i></i><i></i><i></i></div><div class="progress"><b></b></div></div></div>`;

  $('showMe').addEventListener('click', () => {
    $('showMe').disabled = true;
    later(() => bubble(text.answer, true), 500);
    later(() => {
      const tile = document.createElement('div');
      tile.className = 'tile';
      tile.style.setProperty('--tile', colors[state.selected]);
      tile.innerHTML = `${miniScreen()}<em>${text.theirScreen.replace('{name}', person())}</em>`;
      tile.addEventListener('click', () => {
        $('big').innerHTML = miniScreen();
        lightbox.hidden = false;
      });
      tiles.appendChild(tile);
    }, 1300);
  });

  const closeLightbox = () => { lightbox.hidden = true; };
  lightbox.addEventListener('click', (e) => { if (!$('big').contains(e.target)) closeLightbox(); });

  const closeRoom = () => {
    clearTimers();
    closeLightbox();
    setPhase('idle');
    say('closed');
  };
  $('roomClose').addEventListener('click', closeRoom);

  // The edge itself.
  edge.addEventListener('pointerenter', (e) => { if (e.pointerType !== 'touch') rest(); });
  edge.addEventListener('pointerleave', (e) => {
    if (e.pointerType === 'touch') return;
    if (e.clientX >= desk.getBoundingClientRect().right - 1) bump();
    leave();
  });
  edge.addEventListener('click', bump);
  edge.addEventListener('wheel', (e) => {
    if (state.phase !== 'edge') return;
    e.preventDefault();
    if (Math.abs(e.deltaY) < 4) return;
    const next = Math.max(0, Math.min(text.people.length - 1, state.selected + Math.sign(e.deltaY)));
    if (next !== state.selected && !state.wheelLock) {
      state.selected = next;
      drawDial();
      state.wheelLock = true;
      setTimeout(() => { state.wheelLock = false; }, 180);
    }
  }, { passive: false });
  edge.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); bump(); }
    if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && state.phase === 'edge') {
      e.preventDefault();
      state.selected = Math.max(0, Math.min(text.people.length - 1, state.selected + (e.key === 'ArrowDown' ? 1 : -1)));
      drawDial();
    }
  });
  edge.addEventListener('focus', rest);
  edge.addEventListener('blur', leave);

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if (!lightbox.hidden) closeLightbox();
    else if (state.phase === 'room') closeRoom();
  });

  // Without a pointer on the edge (a phone, a mouse far away): the same steps, played.
  $('fallback').addEventListener('click', () => {
    if (state.phase === 'room') closeRoom();
    clearTimers();
    setPhase('idle');
    rest();
    desk.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    [500, 850, 1200].forEach((ms) => later(() => { if (state.phase === 'edge') bump(); }, ms));
  });
})();
