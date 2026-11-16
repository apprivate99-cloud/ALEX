/* Nearby — find the best restaurants & bars around you and book on their own site.
 * Data: OpenStreetMap via the Overpass API (no API key required).
 * Geocoding for manual search: Nominatim.
 */
(() => {
  'use strict';

  // ---------- Config ----------
  const OVERPASS_ENDPOINTS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
  ];
  const NOMINATIM = 'https://nominatim.openstreetmap.org/search';
  const RESTAURANT_TAGS = ['restaurant'];
  const BAR_TAGS = ['bar', 'pub', 'biergarten', 'nightclub'];
  const MAX_RESULTS = 300;

  // ---------- State ----------
  const state = {
    center: null,          // {lat, lng, label}
    places: [],
    type: 'all',
    radius: 1000,
    sort: 'best',
    filter: '',
    bookableOnly: false,
    activeId: null,
  };

  // ---------- DOM ----------
  const $ = (sel) => document.querySelector(sel);
  const el = {
    locateBtn: $('#locateBtn'),
    placeForm: $('#placeForm'),
    placeInput: $('#placeInput'),
    radius: $('#radius'),
    sort: $('#sort'),
    filterText: $('#filterText'),
    bookableOnly: $('#bookableOnly'),
    status: $('#status'),
    list: $('#list'),
    detail: $('#detail'),
    detailBody: $('#detailBody'),
    chips: document.querySelectorAll('.chip'),
  };

  // ---------- Map ----------
  const map = L.map('map', { zoomControl: true }).setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);
  const markersLayer = L.layerGroup().addTo(map);
  let meMarker = null;
  let radiusCircle = null;
  const markerById = new Map();

  // ---------- Utils ----------
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));

  function safeUrl(raw) {
    if (!raw) return null;
    let s = String(raw).trim().split(/\s*;\s*/)[0];
    if (!s) return null;
    if (!/^[a-z][a-z0-9+.-]*:/i.test(s)) s = 'https://' + s.replace(/^\/+/, '');
    try {
      const u = new URL(s);
      return (u.protocol === 'http:' || u.protocol === 'https:') ? u.href : null;
    } catch { return null; }
  }

  function haversine(a, b) {
    const R = 6371000, rad = Math.PI / 180;
    const dLat = (b.lat - a.lat) * rad, dLng = (b.lng - a.lng) * rad;
    const h = Math.sin(dLat / 2) ** 2 +
      Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }

  const fmtDist = (m) => m < 1000 ? `${Math.round(m / 10) * 10} m` : `${(m / 1000).toFixed(1)} km`;
  const walkMins = (m) => Math.max(1, Math.round(m / 80));
  const titleCase = (s) => s.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

  // ---------- Opening hours (best-effort parser for common OSM formats) ----------
  const DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

  function parseHours(str) {
    if (!str) return null;
    const s = str.trim();
    if (s === '24/7') return { always: true };
    const week = Array.from({ length: 7 }, () => null); // null = unknown, [] = closed
    for (const rawRule of s.split(';')) {
      const rule = rawRule.trim();
      if (!rule) continue;
      const m = rule.match(/^((?:(?:Mo|Tu|We|Th|Fr|Sa|Su)(?:\s*-\s*(?:Mo|Tu|We|Th|Fr|Sa|Su))?\s*,?\s*)+)\s+(.+)$/);
      let days, times;
      if (m) { days = expandDays(m[1]); times = m[2].trim(); }
      else if (/^\d/.test(rule)) { days = [0, 1, 2, 3, 4, 5, 6]; times = rule; }
      else continue; // PH, month rules etc. — ignore
      if (!days) return null;
      if (/^(off|closed)$/i.test(times)) { days.forEach((d) => { week[d] = []; }); continue; }
      const ranges = [];
      for (const t of times.split(',')) {
        const tm = t.trim().match(/^(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\+?$/);
        if (!tm) return null;
        ranges.push([+tm[1] * 60 + +tm[2], +tm[3] * 60 + +tm[4]]);
      }
      days.forEach((d) => { week[d] = ranges; });
    }
    return week.some((d) => d !== null) ? { week } : null;
  }

  function expandDays(spec) {
    const out = new Set();
    for (const part of spec.split(',')) {
      const p = part.trim();
      if (!p) continue;
      const [a, b] = p.split('-').map((x) => DAYS.indexOf(x.trim()));
      if (a < 0 || (b !== undefined && b < 0)) return null;
      if (b === undefined) { out.add(a); continue; }
      for (let i = a; ; i = (i + 1) % 7) { out.add(i); if (i === b) break; }
    }
    return [...out];
  }

  /** returns true / false / null(unknown) */
  function isOpenNow(parsed, now = new Date()) {
    if (!parsed) return null;
    if (parsed.always) return true;
    const day = (now.getDay() + 6) % 7; // Monday = 0
    const mins = now.getHours() * 60 + now.getMinutes();
    const today = parsed.week[day];
    const yesterday = parsed.week[(day + 6) % 7];
    if (today === null && yesterday === null) return null;
    // ranges that started today
    for (const [o, c] of today || []) {
      const close = c <= o ? c + 1440 : c;
      if (mins >= o && mins < close) return true;
    }
    // overnight ranges that started yesterday
    for (const [o, c] of yesterday || []) {
      if (c <= o && mins < c) return true;
    }
    return today === null ? null : false;
  }

  // ---------- Data ----------
  function buildQuery({ lat, lng }, radius) {
    const re = [...RESTAURANT_TAGS, ...BAR_TAGS].join('|');
    return `[out:json][timeout:25];
nwr(around:${radius},${lat.toFixed(6)},${lng.toFixed(6)})["amenity"~"^(${re})$"]["name"];
out center tags ${MAX_RESULTS * 2};`;
  }

  async function fetchOverpass(query) {
    let lastErr;
    for (const url of OVERPASS_ENDPOINTS) {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 30000);
        const res = await fetch(url, {
          method: 'POST',
          body: 'data=' + encodeURIComponent(query),
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          signal: ctrl.signal,
        });
        clearTimeout(timer);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
      } catch (e) { lastErr = e; }
    }
    throw lastErr || new Error('No data source reachable');
  }

  function bookingInfo(t) {
    const reservationUrl = safeUrl(t['reservation:url'] || t['reservation:website'] || t['website:booking'] || t['booking']);
    const website = safeUrl(t.website || t['contact:website'] || t.url);
    const social = safeUrl(t['contact:facebook'] || t.facebook || t['contact:instagram']);
    const policy = t.reservation || null; // yes | no | recommended | required | only
    if (reservationUrl) return { url: reservationUrl, kind: 'direct', policy, website };
    if (website) return { url: website, kind: 'website', policy, website };
    if (social) return { url: social, kind: 'social', policy, website: null };
    return { url: null, kind: 'none', policy, website: null };
  }

  function normalise(el) {
    const t = el.tags || {};
    const lat = el.lat ?? el.center?.lat;
    const lng = el.lon ?? el.center?.lon;
    if (lat == null || lng == null || !t.name) return null;
    const category = BAR_TAGS.includes(t.amenity) ? 'bar' : 'restaurant';
    const cuisine = (t.cuisine || '').split(';').map((c) => c.trim()).filter(Boolean).map(titleCase);
    const addr = [
      [t['addr:housenumber'], t['addr:street']].filter(Boolean).join(' '),
      t['addr:city'] || t['addr:suburb'],
      t['addr:postcode'],
    ].filter(Boolean).join(', ');
    const hoursParsed = parseHours(t.opening_hours);
    const p = {
      id: `${el.type}/${el.id}`,
      name: t.name,
      amenity: t.amenity,
      category,
      cuisine,
      lat, lng,
      address: addr,
      phone: t.phone || t['contact:phone'] || null,
      hours: t.opening_hours || null,
      openNow: isOpenNow(hoursParsed),
      booking: bookingInfo(t),
      outdoor: t.outdoor_seating === 'yes',
      wheelchair: t.wheelchair === 'yes',
      vegetarian: /yes|only/.test(t['diet:vegetarian'] || ''),
      vegan: /yes|only/.test(t['diet:vegan'] || ''),
      chain: Boolean(t.brand || t['brand:wikidata']),
      notable: Boolean(t.wikipedia || t.wikidata || t.michelin || t['michelin:stars'] || t.stars),
      description: t.description || null,
      tags: t,
    };
    return p;
  }

  /**
   * "Best match" score, 0–10. OpenStreetMap has no star ratings, so we rank on
   * signals that correlate with established, well-run venues: notable/listed,
   * independent (not a chain), takes reservations, has a website, published hours,
   * cuisine info, plus a gentle penalty for distance.
   */
  function scorePlace(p, radius) {
    let s = 4;
    if (p.notable) s += 2;
    if (!p.chain) s += 1;
    else s -= 0.5;
    if (p.booking.kind === 'direct') s += 1.5;
    else if (p.booking.kind === 'website') s += 1;
    else if (p.booking.kind === 'social') s += 0.3;
    if (['yes', 'recommended', 'required', 'only'].includes(p.booking.policy)) s += 0.7;
    if (p.hours) s += 0.6;
    if (p.cuisine.length) s += 0.4;
    if (p.phone) s += 0.3;
    if (p.address) s += 0.2;
    if (p.outdoor) s += 0.2;
    if (p.wheelchair) s += 0.1;
    if (p.amenity === 'nightclub' || p.amenity === 'biergarten') s -= 0.2;
    const distFactor = 1 - Math.min(1, p.distance / Math.max(radius, 1)) * 0.25;
    return Math.max(0, Math.min(10, s * distFactor));
  }

  // ---------- Search flow ----------
  async function search(center) {
    state.center = center;
    setLoading(`Finding restaurants & bars near ${center.label || 'you'}…`);
    showMe(center);
    try {
      const data = await fetchOverpass(buildQuery(center, state.radius));
      const seen = new Set();
      state.places = (data.elements || [])
        .map(normalise)
        .filter(Boolean)
        .filter((p) => {
          const key = p.name.toLowerCase() + '|' + p.lat.toFixed(4) + '|' + p.lng.toFixed(4);
          if (seen.has(key)) return false;
          seen.add(key); return true;
        })
        .map((p) => {
          p.distance = haversine(center, p);
          p.score = scorePlace(p, state.radius);
          return p;
        });
      render(true);
    } catch (err) {
      console.error(err);
      setError('Couldn’t load places right now',
        'The map data service may be busy. Please try again in a moment.');
    }
  }

  function locate() {
    if (!('geolocation' in navigator)) {
      setError('Location isn’t available', 'Your browser doesn’t support GPS location. Enter a town or postcode instead.');
      return;
    }
    el.locateBtn.disabled = true;
    setLoading('Getting your location…');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        el.locateBtn.disabled = false;
        search({ lat: pos.coords.latitude, lng: pos.coords.longitude, label: 'you' });
      },
      (err) => {
        el.locateBtn.disabled = false;
        const msg = err.code === 1
          ? 'Location permission was denied. Allow location access in your browser, or enter a town or postcode above.'
          : 'We couldn’t determine your location. Try again, or enter a town or postcode above.';
        setError('Couldn’t get your location', msg);
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 },
    );
  }

  async function geocode(q) {
    setLoading(`Looking up “${q}”…`);
    try {
      const url = `${NOMINATIM}?format=jsonv2&limit=1&q=${encodeURIComponent(q)}`;
      const res = await fetch(url, { headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const [hit] = await res.json();
      if (!hit) { setError('Place not found', `We couldn’t find “${q}”. Try a different town or postcode.`); return; }
      const label = hit.display_name.split(',').slice(0, 2).join(',');
      search({ lat: +hit.lat, lng: +hit.lon, label });
    } catch (e) {
      console.error(e);
      setError('Search failed', 'The place search service didn’t respond. Please try again.');
    }
  }

  // ---------- Rendering ----------
  function setLoading(text) {
    el.status.className = 'status';
    el.status.innerHTML = `<p><span class="spinner"></span>${esc(text)}</p>`;
    el.status.hidden = false;
    el.list.innerHTML = '';
  }

  function setError(title, text) {
    el.status.className = 'status error';
    el.status.innerHTML = `<h2>${esc(title)}</h2><p>${esc(text)}</p>`;
    el.status.hidden = false;
    el.list.innerHTML = '';
  }

  function showMe(center) {
    if (meMarker) meMarker.remove();
    if (radiusCircle) radiusCircle.remove();
    meMarker = L.marker([center.lat, center.lng], {
      icon: L.divIcon({ className: '', html: '<div class="me-dot"></div>', iconSize: [16, 16], iconAnchor: [8, 8] }),
      zIndexOffset: 1000, keyboard: false,
    }).addTo(map).bindTooltip(center.label === 'you' ? 'You are here' : esc(center.label));
    radiusCircle = L.circle([center.lat, center.lng], {
      radius: state.radius, color: '#c2410c', weight: 1, fillOpacity: 0.04, interactive: false,
    }).addTo(map);
    map.fitBounds(radiusCircle.getBounds(), { padding: [20, 20] });
  }

  function visiblePlaces() {
    const f = state.filter.trim().toLowerCase();
    let list = state.places.filter((p) => {
      if (p.distance > state.radius) return false;
      if (state.type !== 'all' && p.category !== state.type) return false;
      if (state.bookableOnly && !(p.booking.kind === 'direct' || p.booking.kind === 'website')) return false;
      if (f) {
        const hay = [p.name, p.amenity, ...p.cuisine, p.vegan ? 'vegan' : '', p.vegetarian ? 'vegetarian' : ''].join(' ').toLowerCase();
        if (!hay.includes(f)) return false;
      }
      return true;
    });
    const by = {
      best: (a, b) => b.score - a.score || a.distance - b.distance,
      distance: (a, b) => a.distance - b.distance,
      name: (a, b) => a.name.localeCompare(b.name),
    }[state.sort];
    return list.sort(by).slice(0, MAX_RESULTS);
  }

  function bookButton(p, extraClass = '') {
    const b = p.booking;
    if (b.kind === 'direct' || b.kind === 'website') {
      const label = b.kind === 'direct' || ['yes', 'recommended', 'required', 'only'].includes(b.policy)
        ? 'Book a table' : 'Book / visit website';
      return `<a class="btn btn-primary ${extraClass}" href="${esc(b.url)}" target="_blank" rel="noopener noreferrer" data-book>${label} ↗</a>`;
    }
    if (b.kind === 'social') {
      return `<a class="btn btn-primary ${extraClass}" href="${esc(b.url)}" target="_blank" rel="noopener noreferrer" data-book>Contact to book ↗</a>`;
    }
    const q = encodeURIComponent(`${p.name} ${p.address || ''} book a table`);
    return `<a class="btn ${extraClass}" href="https://www.google.com/search?q=${q}" target="_blank" rel="noopener noreferrer" data-book>Find booking site ↗</a>`;
  }

  function badges(p) {
    const out = [`<span class="badge type-${p.category}">${esc(titleCase(p.amenity))}</span>`];
    p.cuisine.slice(0, 3).forEach((c) => out.push(`<span class="badge">${esc(c)}</span>`));
    if (p.openNow === true) out.push('<span class="badge open">Open now</span>');
    if (p.openNow === false) out.push('<span class="badge">Closed now</span>');
    if (p.booking.policy === 'no') out.push('<span class="badge">Walk-in only</span>');
    if (p.vegan) out.push('<span class="badge">Vegan options</span>');
    else if (p.vegetarian) out.push('<span class="badge">Vegetarian options</span>');
    if (p.outdoor) out.push('<span class="badge">Outdoor seating</span>');
    return out.join('');
  }

  function render(fit = false) {
    const list = visiblePlaces();
    markersLayer.clearLayers();
    markerById.clear();

    if (!state.center) return;
    if (!list.length) {
      const what = state.type === 'bar' ? 'bars' : state.type === 'restaurant' ? 'restaurants' : 'restaurants or bars';
      setError(`No ${what} found`, 'Try widening the search radius or clearing your filters.');
      return;
    }

    el.status.className = 'status';
    el.status.hidden = false;
    const label = state.center.label === 'you' ? 'you' : state.center.label;
    el.status.innerHTML = `<p><strong>${list.length}</strong> place${list.length === 1 ? '' : 's'} within ${fmtDist(state.radius)} of ${esc(label)}${state.sort === 'best' ? ' · ranked by best match' : ''}</p>`;

    el.list.innerHTML = list.map((p, i) => `
      <li class="card" tabindex="0" data-id="${esc(p.id)}">
        <div class="card-head">
          <h3><span class="rank">${i + 1}.</span>${esc(p.name)}</h3>
          ${state.sort === 'best' ? `<span class="score" title="Best-match score">${p.score.toFixed(1)}</span>` : ''}
        </div>
        <div class="meta">${fmtDist(p.distance)} · ${walkMins(p.distance)} min walk${p.address ? ' · ' + esc(p.address) : ''}</div>
        <div class="badges">${badges(p)}</div>
        <div class="card-actions">
          ${bookButton(p)}
          <button class="btn" type="button" data-details>Details</button>
        </div>
      </li>`).join('');

    list.forEach((p, i) => {
      const m = L.marker([p.lat, p.lng], {
        icon: L.divIcon({
          className: '',
          html: `<div class="pin ${p.category}"><span>${i < 99 ? i + 1 : ''}</span></div>`,
          iconSize: [28, 28], iconAnchor: [14, 28], popupAnchor: [0, -26],
        }),
        title: p.name,
        riseOnHover: true,
      });
      m.bindPopup(`<div class="popup"><h4>${esc(p.name)}</h4>
        <div>${esc(titleCase(p.amenity))}${p.cuisine.length ? ' · ' + esc(p.cuisine.join(', ')) : ''}</div>
        <div>${fmtDist(p.distance)} away</div>
        ${bookButton(p)} <button class="btn" type="button" data-popup-details="${esc(p.id)}">Details</button></div>`);
      m.on('click', () => highlight(p.id, false));
      m.addTo(markersLayer);
      markerById.set(p.id, m);
    });

    if (fit && radiusCircle) map.fitBounds(radiusCircle.getBounds(), { padding: [20, 20] });
  }

  function highlight(id, pan = true) {
    state.activeId = id;
    document.querySelectorAll('.card.highlight').forEach((c) => c.classList.remove('highlight'));
    const card = el.list.querySelector(`[data-id="${CSS.escape(id)}"]`);
    if (card) {
      card.classList.add('highlight');
      if (!pan) card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    const m = markerById.get(id);
    if (m && pan) {
      map.setView(m.getLatLng(), Math.max(map.getZoom(), 16), { animate: true });
      m.openPopup();
    }
  }

  function openDetails(id) {
    const p = state.places.find((x) => x.id === id);
    if (!p) return;
    const t = p.tags;
    const rows = [];
    rows.push(['Type', esc(titleCase(p.amenity)) + (p.cuisine.length ? ' · ' + esc(p.cuisine.join(', ')) : '')]);
    rows.push(['Distance', `${fmtDist(p.distance)} (≈${walkMins(p.distance)} min walk)`]);
    if (p.address) rows.push(['Address', esc(p.address)]);
    if (p.phone) rows.push(['Phone', `<a href="tel:${esc(p.phone.replace(/[^\d+]/g, ''))}">${esc(p.phone)}</a>`]);
    if (p.hours) {
      const status = p.openNow === true ? ' <strong class="badge open">Open now</strong>'
        : p.openNow === false ? ' <strong class="badge">Closed now</strong>' : '';
      rows.push(['Hours', `<span class="hours">${esc(p.hours.replace(/;\s*/g, '\n'))}</span>${status}`]);
    }
    if (p.booking.policy) {
      const pol = { yes: 'Takes reservations', no: 'No reservations (walk-in)', recommended: 'Reservations recommended', required: 'Reservations required', only: 'Reservations only' }[p.booking.policy] || p.booking.policy;
      rows.push(['Bookings', esc(pol)]);
    }
    if (p.booking.website) rows.push(['Website', `<a href="${esc(p.booking.website)}" target="_blank" rel="noopener noreferrer">${esc(new URL(p.booking.website).hostname)}</a>`]);
    const extras = [p.outdoor && 'Outdoor seating', p.wheelchair && 'Wheelchair accessible', p.vegan && 'Vegan options', !p.vegan && p.vegetarian && 'Vegetarian options', t.takeaway === 'yes' && 'Takeaway', t.delivery === 'yes' && 'Delivery'].filter(Boolean);
    if (extras.length) rows.push(['Features', esc(extras.join(' · '))]);
    if (p.description) rows.push(['About', esc(p.description)]);

    const dir = `https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lng}`;
    const note = p.booking.kind === 'none'
      ? 'This venue hasn’t listed a booking site, so we’ll search the web for it.'
      : 'You’ll book directly with the venue on their own website.';

    el.detailBody.innerHTML = `
      <h2>${esc(p.name)}</h2>
      <div class="badges">${badges(p)}</div>
      <dl>${rows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl>
      <div class="card-actions">
        ${bookButton(p)}
        <a class="btn" href="${dir}" target="_blank" rel="noopener noreferrer">Directions ↗</a>
      </div>
      <p class="book-note">${note}</p>`;
    if (typeof el.detail.showModal === 'function') el.detail.showModal();
    else el.detail.setAttribute('open', '');
  }

  // ---------- Events ----------
  el.locateBtn.addEventListener('click', locate);

  el.placeForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = el.placeInput.value.trim();
    if (q) geocode(q);
  });

  el.chips.forEach((chip) => chip.addEventListener('click', () => {
    el.chips.forEach((c) => { c.classList.toggle('active', c === chip); c.setAttribute('aria-selected', c === chip); });
    state.type = chip.dataset.type;
    render();
  }));

  el.radius.addEventListener('change', () => {
    const prev = state.radius;
    state.radius = +el.radius.value;
    if (!state.center) return;
    if (state.radius > prev) search(state.center);  // need more data
    else {
      state.places.forEach((p) => { p.score = scorePlace(p, state.radius); });
      showMe(state.center);
      render(true);
    }
  });

  el.sort.addEventListener('change', () => { state.sort = el.sort.value; render(); });

  let filterTimer;
  el.filterText.addEventListener('input', () => {
    clearTimeout(filterTimer);
    filterTimer = setTimeout(() => { state.filter = el.filterText.value; render(); }, 150);
  });

  el.bookableOnly.addEventListener('change', () => { state.bookableOnly = el.bookableOnly.checked; render(); });

  el.list.addEventListener('click', (e) => {
    const card = e.target.closest('.card');
    if (!card) return;
    if (e.target.closest('[data-book]')) return; // let link open
    if (e.target.closest('[data-details]')) { openDetails(card.dataset.id); return; }
    highlight(card.dataset.id);
  });
  el.list.addEventListener('keydown', (e) => {
    const card = e.target.closest('.card');
    if (card && e.target === card && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      openDetails(card.dataset.id);
    }
  });

  map.on('popupopen', (e) => {
    const btn = e.popup.getElement().querySelector('[data-popup-details]');
    if (btn) btn.addEventListener('click', () => openDetails(btn.dataset.popupDetails));
  });

  el.detail.addEventListener('click', (e) => { if (e.target === el.detail) el.detail.close(); });

  // Expose for tests
  window.__nearby = { parseHours, isOpenNow, safeUrl, state };
})();
