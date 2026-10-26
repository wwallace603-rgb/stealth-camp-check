#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');

const WEB = 'https://carsteader.com/tools/stealth-camp-check/';
const GUIDES = {
  legal:   'https://carsteader.com/legal-stealth-camping-usa/',
  gear:    'https://carsteader.com/stealth-camping-gear-list/',
  windows: 'https://carsteader.com/stealth-camping-windows-covers/'
};

const DATA = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'stealth_camp_check', 'states.json'), 'utf8'));
const BLM = new Set(DATA.blmStates);
const STATUS_LABEL = { ok: 'OK', limited: 'LIMITED', no: 'NO', signs: 'SIGNS GOVERN' };

const useColor = process.stdout.isTTY && !process.env.NO_COLOR;
const c = (code, s) => (useColor ? '\x1b[' + code + 'm' + s + '\x1b[0m' : String(s));
const statusColor = { ok: '32', limited: '33', no: '31', signs: '97' };

function findState(arg) {
  const a = arg.trim().toLowerCase();
  return DATA.states.find(function (s) { return s.ab.toLowerCase() === a || s.name.toLowerCase() === a; });
}

function printDetail(s) {
  console.log('');
  console.log(c('1', s.name));
  console.log('Rest areas: ' + c(statusColor[s.status], STATUS_LABEL[s.status]) + (s.limit ? ' — ' + s.limit : ''));
  if (s.note) console.log('  ' + s.note);
  console.log('');
  console.log('  BLM land ........ ' + (BLM.has(s.ab) ? 'Yes — 14-day rule applies (western states)' : 'Not a primary BLM state'));
  console.log('  National forests  Dispersed camping generally OK unless posted (7–21 day limits vary)');
  console.log('  Big-box lots .... Private property, store-by-store — ask at the entrance');
  if (s.src) { console.log(''); console.log('  Source: ' + s.src); }
  console.log('');
  console.log(c('36', 'More from CarSteader:'));
  console.log('  Web tool ........ ' + WEB + '?state=' + s.ab);
  console.log('  Legal guide ..... ' + GUIDES.legal);
  console.log('  Stealth gear .... ' + GUIDES.gear);
  console.log('');
}

function printList() {
  console.log('');
  for (const s of DATA.states) {
    const ab = c('1', s.ab.padEnd(3));
    const st = c(statusColor[s.status], STATUS_LABEL[s.status].padEnd(12));
    console.log('  ' + ab + ' ' + st + ' ' + (s.limit || '—').slice(0, 52));
  }
  console.log('');
  console.log(c('36', WEB));
  console.log('');
}

function usage() {
  console.log([
    '',
    c('1', 'stealth-camp-check') + ' — overnight parking & rest area rules by state',
    '',
    'Usage:',
    '  stealth-camp-check <state>         Rules for one state (code or name), e.g. "tx" or "Texas"',
    '  stealth-camp-check --list          Table of all 50 states + DC',
    '  stealth-camp-check <state> --json  Raw JSON for one state',
    '',
    'Examples:',
    '  stealth-camp-check tx',
    '  stealth-camp-check georgia',
    '  stealth-camp-check --list',
    '',
    c('36', 'Interactive web tool (all states): ') + WEB,
    ''
  ].join('\n'));
}

const args = process.argv.slice(2);
if (args.length === 0 || args.includes('--help') || args.includes('-h')) { usage(); process.exit(0); }
if (args.includes('--list') || args.includes('-l')) { printList(); process.exit(0); }

const wantJson = args.includes('--json');
const stateArg = args.find(function (a) { return !a.startsWith('-'); });
if (!stateArg) { usage(); process.exit(1); }
const s = findState(stateArg);
if (!s) { console.error('Unknown state: "' + stateArg + '". Try --list to see codes.'); process.exit(1); }
if (wantJson) { console.log(JSON.stringify(s, null, 2)); process.exit(0); }
printDetail(s);
