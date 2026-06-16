// ── Biergerpakt Podcast – app logic ──────────────────────
let user = {};
let selectedEpisode = null;

// Quiz state
let answers = [];
let wrongIndices = [];
let retryIndices = [];
let retryPos = 0;
let curIndex = 0;
let isRetry = false;

// Transcript / audio sync state
let segEls = [];
let segTimes = [];
let activeSeg = -1;
let userScrolling = false;
let userScrollTimer = null;

// ── Helpers ──────────────────────────────────────────────
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(function (s) { s.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function show(id) { document.getElementById(id).classList.remove('hidden'); }
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// ── Registration ─────────────────────────────────────────
function doRegister() {
  var fn = document.getElementById('inp-first').value.trim();
  var ln = document.getElementById('inp-last').value.trim();
  var em = document.getElementById('inp-email').value.trim();
  var ok = true;

  function check(val, inputId, errId, testFn) {
    var inp = document.getElementById(inputId);
    var err = document.getElementById(errId);
    if (!testFn(val)) { inp.classList.add('error'); err.style.display = 'block'; ok = false; }
    else { inp.classList.remove('error'); err.style.display = 'none'; }
  }
  check(fn, 'inp-first', 'err-first', function (v) { return v.length > 0; });
  check(ln, 'inp-last', 'err-last', function (v) { return v.length > 0; });
  if (!ok) return;

  user = { firstName: fn, lastName: ln, email: em };
  renderEpisodeList();
  showScreen('screen-episodes');
}

// ── Episode list ─────────────────────────────────────────
function renderEpisodeList() {
  var grid = document.getElementById('episode-grid');
  grid.innerHTML = '';
  EPISODES.forEach(function (ep) {
    var card = document.createElement('div');
    card.className = 'ep-list-card';
    card.innerHTML =
      '<div class="ep-list-badge">' + esc(ep.number) + '</div>' +
      '<div class="ep-list-title">' + esc(ep.title) + '</div>' +
      '<div class="ep-list-desc">' + esc(ep.description) + '</div>' +
      '<button class="btn ep-list-btn">Listen &amp; take the quiz &rarr;</button>';
    card.querySelector('button').addEventListener('click', function () { selectEpisode(ep.id); });
    grid.appendChild(card);
  });
}

// ── Select episode ───────────────────────────────────────
function selectEpisode(id) {
  selectedEpisode = EPISODES.find(function (e) { return e.id === id; });
  renderEpisodeDetail();
  showScreen('screen-episode');
}

// ── Episode detail (player + transcript + topics) ────────
function renderEpisodeDetail() {
  var ep = selectedEpisode;
  document.getElementById('ep-badge').textContent = ep.number;
  document.getElementById('ep-title').textContent = ep.title;
  document.getElementById('ep-description').textContent = ep.description;

  // Audio
  var audio = document.getElementById('ep-audio');
  audio.pause();
  audio.src = ep.audio;
  audio.load();

  // Transcript
  var tw = document.getElementById('transcript');
  tw.innerHTML = '';
  tw.scrollTop = 0;
  segEls = [];
  segTimes = [];
  activeSeg = -1;
  var lastSpeaker = null;
  ep.segments.forEach(function (seg, i) {
    var line = document.createElement('button');
    line.className = 't-line';
    line.type = 'button';
    var speakerTag = '';
    if (seg.speaker !== lastSpeaker) {
      speakerTag = '<span class="t-speaker ' + seg.speaker + '">' + esc(seg.speaker) + '</span>';
      lastSpeaker = seg.speaker;
    }
    line.innerHTML = speakerTag + '<span class="t-text">' + esc(seg.text) + '</span>';
    line.addEventListener('click', function () {
      audio.currentTime = seg.t + 0.01;
      audio.play();
      userScrolling = false;
      setActiveSeg(i, true);
    });
    tw.appendChild(line);
    segEls.push(line);
    segTimes.push(seg.t);
  });

  // Topics
  var chips = document.getElementById('ep-topics');
  chips.innerHTML = '';
  ep.topics.forEach(function (t) {
    var c = document.createElement('div');
    c.className = 'topic-chip';
    c.textContent = t;
    chips.appendChild(c);
  });
}

// ── Karaoke highlighting ─────────────────────────────────
function findSegIndex(time) {
  // last segment whose start time <= current time (binary search)
  var lo = 0, hi = segTimes.length - 1, res = 0;
  if (hi < 0) return -1;
  while (lo <= hi) {
    var mid = (lo + hi) >> 1;
    if (segTimes[mid] <= time) { res = mid; lo = mid + 1; }
    else { hi = mid - 1; }
  }
  return res;
}
function setActiveSeg(i, forceScroll) {
  if (i === activeSeg && !forceScroll) return;
  if (activeSeg >= 0 && segEls[activeSeg]) {
    segEls[activeSeg].classList.remove('active');
    segEls[activeSeg].classList.add('spoken');
  }
  // mark everything before i as spoken, after as not
  segEls.forEach(function (el, k) {
    if (k < i) el.classList.add('spoken'); else el.classList.remove('spoken');
  });
  activeSeg = i;
  if (i < 0 || !segEls[i]) return;
  segEls[i].classList.remove('spoken');
  segEls[i].classList.add('active');
  var follow = document.getElementById('follow-chk').checked;
  if (follow && (!userScrolling || forceScroll)) {
    centerLine(segEls[i]);
  }
}

// Scroll a transcript line to the vertical centre of the script box.
// Uses bounding rectangles so it is correct regardless of page layout.
function centerLine(el) {
  var tw = document.getElementById('transcript');
  if (!tw || !el) return;
  var cRect = tw.getBoundingClientRect();
  var eRect = el.getBoundingClientRect();
  var target = tw.scrollTop + (eRect.top - cRect.top) - (tw.clientHeight / 2 - el.clientHeight / 2);
  if (target < 0) target = 0;
  tw.scrollTo({ top: target, behavior: 'smooth' });
}
function onTimeUpdate() {
  var audio = document.getElementById('ep-audio');
  var i = findSegIndex(audio.currentTime);
  if (i !== activeSeg) setActiveSeg(i, false);
}

// ── Quiz ─────────────────────────────────────────────────
function startQuiz() {
  answers = new Array(selectedEpisode.questions.length).fill(-1);
  wrongIndices = [];
  curIndex = 0;
  isRetry = false;
  document.getElementById('q-label').textContent = selectedEpisode.number + ' – Biergerpakt Podcast';
  document.getElementById('ep-audio').pause();
  showScreen('screen-quiz');
  renderQuestion(0);
}
function renderQuestion(idx) {
  var q = selectedEpisode.questions[idx];
  var total = selectedEpisode.questions.length;
  document.getElementById('q-counter').textContent = 'Question ' + (idx + 1) + ' of ' + total;
  document.getElementById('q-eyebrow').textContent = 'Question ' + (idx + 1);
  document.getElementById('q-text').textContent = q.text;
  document.getElementById('q-progress').style.width = (((idx + 1) / total) * 100) + '%';

  var optWrap = document.getElementById('q-options');
  optWrap.innerHTML = '';
  var letters = ['A', 'B', 'C', 'D'];
  q.options.forEach(function (text, i) {
    var div = document.createElement('div');
    div.className = 'option';
    div.innerHTML = '<div class="opt-letter">' + letters[i] + '</div><div class="opt-text">' + esc(text) + '</div>';
    div.addEventListener('click', function () { selectAnswer(i); });
    optWrap.appendChild(div);
  });
  var fb = document.getElementById('q-feedback');
  fb.className = 'feedback';
  fb.textContent = '';
  hide('btn-next');
}
function selectAnswer(chosen) {
  if (!document.getElementById('btn-next').classList.contains('hidden')) return;
  var q = selectedEpisode.questions[curIndex];
  answers[curIndex] = chosen;

  document.querySelectorAll('.option').forEach(function (el) {
    el.style.cursor = 'default';
    el.replaceWith(el.cloneNode(true));
  });
  document.querySelectorAll('.option').forEach(function (el, i) {
    if (i === q.correct) el.classList.add('correct');
    if (i === chosen && i !== q.correct) el.classList.add('wrong');
  });

  var fb = document.getElementById('q-feedback');
  if (chosen === q.correct) {
    fb.className = 'feedback show ok';
    fb.innerHTML = '<strong>✅ Correct!</strong> ' + esc(q.explanation);
  } else {
    fb.className = 'feedback show fail';
    fb.innerHTML = '<strong>❌ Not quite.</strong> The correct answer is: <strong>' +
      esc(q.options[q.correct]) + '</strong>. ' + esc(q.explanation);
  }
  show('btn-next');
}
function nextQuestion() {
  if (isRetry) {
    retryPos++;
    if (retryPos < retryIndices.length) { curIndex = retryIndices[retryPos]; renderQuestion(curIndex); }
    else { showResults(); }
  } else {
    curIndex++;
    if (curIndex < selectedEpisode.questions.length) { renderQuestion(curIndex); }
    else { showResults(); }
  }
}

// ── Results ──────────────────────────────────────────────
function showResults() {
  wrongIndices = [];
  answers.forEach(function (ans, i) {
    if (ans !== selectedEpisode.questions[i].correct) wrongIndices.push(i);
  });
  var total = selectedEpisode.questions.length;
  var nCorrect = total - wrongIndices.length;

  document.getElementById('score-n').textContent = nCorrect;
  document.getElementById('score-d').textContent = 'of ' + total;
  var ring = document.getElementById('score-ring');

  if (nCorrect === total) {
    ring.style.background = 'var(--green)';
    document.getElementById('score-title').textContent = '🎉 Excellent – all correct!';
    document.getElementById('score-msg').textContent = 'You answered every question correctly. You can now download your certificate of participation.';
    hide('retry-card');
    show('success-banner');
  } else {
    ring.style.background = 'var(--orange)';
    document.getElementById('score-title').textContent = nCorrect + ' of ' + total + ' questions correct';
    document.getElementById('score-msg').textContent = 'To earn the certificate, every question must be correct. Listen again to the relevant parts of the episode, then retry the questions below.';
    var list = document.getElementById('wrong-list');
    list.innerHTML = wrongIndices.map(function (i) {
      return '<div class="wrong-item"><strong>Question ' + (i + 1) + ':</strong> ' + esc(selectedEpisode.questions[i].text) + '</div>';
    }).join('');
    show('retry-card');
    hide('success-banner');
  }
  showScreen('screen-results');
}
function retryWrong() {
  isRetry = true;
  retryIndices = wrongIndices.slice();
  retryPos = 0;
  curIndex = retryIndices[0];
  retryIndices.forEach(function (i) { answers[i] = -1; });
  showScreen('screen-quiz');
  renderQuestion(curIndex);
}

// ── Certificate ──────────────────────────────────────────
function showCertificate() {
  document.getElementById('cert-name-out').textContent = user.firstName + ' ' + user.lastName;
  document.getElementById('cert-episode-out').textContent = selectedEpisode.number + ': ' + selectedEpisode.title;
  var emailLine = document.getElementById('cert-email-line');
  emailLine.innerHTML = user.email ? ('<strong>Email:</strong> ' + esc(user.email) + '<br>') : '';
  document.getElementById('cert-date-out').textContent = new Date().toLocaleDateString('en-GB', {
    day: '2-digit', month: 'long', year: 'numeric'
  });
  showScreen('screen-certificate');
}

// ── Wire up ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('btn-register').addEventListener('click', doRegister);
  ['inp-first', 'inp-last', 'inp-email'].forEach(function (id) {
    document.getElementById(id).addEventListener('keydown', function (e) { if (e.key === 'Enter') doRegister(); });
  });
  document.getElementById('btn-start-quiz').addEventListener('click', startQuiz);
  document.getElementById('btn-next').addEventListener('click', nextQuestion);
  document.getElementById('btn-retry').addEventListener('click', retryWrong);
  document.getElementById('btn-show-cert').addEventListener('click', showCertificate);
  document.getElementById('btn-print').addEventListener('click', function () { window.print(); });
  document.getElementById('btn-back-episode').addEventListener('click', function () { showScreen('screen-episode'); });
  document.getElementById('btn-back-episodes').addEventListener('click', function () {
    document.getElementById('ep-audio').pause(); showScreen('screen-episodes');
  });
  document.getElementById('btn-back-episodes-result').addEventListener('click', function () { showScreen('screen-episodes'); });

  // Audio sync
  var audio = document.getElementById('ep-audio');
  audio.addEventListener('timeupdate', onTimeUpdate);
  audio.addEventListener('seeked', onTimeUpdate);

  // Re-enabling auto-scroll snaps straight back to the highlighted line.
  document.getElementById('follow-chk').addEventListener('change', function () {
    if (this.checked) {
      userScrolling = false;
      if (activeSeg >= 0 && segEls[activeSeg]) centerLine(segEls[activeSeg]);
    }
  });

  // Detect manual scrolling of the transcript -> pause auto-follow briefly,
  // then resume and snap back to the highlighted line.
  var tw = document.getElementById('transcript');
  tw.addEventListener('wheel', markUserScroll, { passive: true });
  tw.addEventListener('touchmove', markUserScroll, { passive: true });
  function markUserScroll() {
    userScrolling = true;
    clearTimeout(userScrollTimer);
    userScrollTimer = setTimeout(function () {
      userScrolling = false;
      // Snap back to the current highlighted line as soon as auto-follow resumes,
      // even if the active line has not changed.
      if (document.getElementById('follow-chk').checked && activeSeg >= 0 && segEls[activeSeg]) {
        centerLine(segEls[activeSeg]);
      }
    }, 4000);
  }
});
