// Adds episode 44 (Blood donation in Luxembourg – dondusang.lu) with its EN/FR/DE content from build/dondusang_content.json.
// Audio, segments and durations are then filled by: node build/replace_audio_elevenlabs.js dondusang en,fr,de
// Run from the project root.
const fs = require('fs');
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const EPISODES = new Function(src + '\nreturn EPISODES;')();
if (EPISODES.find(e => e.key === 'dondusang')) { console.log('dondusang already present'); process.exit(0); }
const c = JSON.parse(fs.readFileSync('build/dondusang_content.json', 'utf8'));
const id = Math.max(...EPISODES.map(e => e.id)) + 1;
EPISODES.push({
  id, key: 'dondusang', number: 'Episode ' + id,
  title: c.en.title, description: c.en.description,
  audio: 'podcast_dondusang.mp3', duration: 0,
  topics: c.en.topics, segments: [], questions: c.en.questions,
  categories: ['health', 'civic'],
  title_fr: c.fr.title, description_fr: c.fr.description, topics_fr: c.fr.topics, questions_fr: c.fr.questions,
  title_de: c.de.title, description_de: c.de.description, topics_de: c.de.topics, questions_de: c.de.questions,
  audio_fr: 'podcast_dondusang_fr.mp3', duration_fr: 0, segments_fr: [],
  audio_de: 'podcast_dondusang_de.mp3', duration_de: 0, segments_de: [],
  segments_lb: []
});
fs.writeFileSync('episodes_data.js', src.slice(0, marker) + 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n');
console.log('added dondusang as episode', id, '— total', EPISODES.length);
