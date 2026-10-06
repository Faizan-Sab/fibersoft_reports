// Bench links public/ into sites/assets before running this command.
// Production installs use the committed release assets; source builds are explicit.
const fs = require('node:fs')
const path = require('node:path')
const assert = require('node:assert/strict')
const app = path.resolve(__dirname, '..', 'fibersoft_reports')
const prefix = '/assets/fibersoft_reports/'

try {
  const index = fs.readFileSync(path.join(app, 'public/frontend/index.html'), 'utf8')
  const page = fs.readFileSync(path.join(app, 'www/fibersoft.html'), 'utf8')
  assert.equal(index, page, 'SPA entry pages differ; rebuild and commit both')
  assert.ok(index.includes('<title>Fibersoft Reports</title>'), 'Missing app title')
  let checked = 0
  for (const match of index.matchAll(/(?:src|href)="(\/assets\/fibersoft_reports\/[^"?#]+)"/g)) {
    const file = path.resolve(app, 'public', match[1].slice(prefix.length))
    assert.ok(file.startsWith(path.join(app, 'public') + path.sep), 'Invalid asset path')
    assert.ok(fs.statSync(file).isFile(), `Missing release asset: ${match[1]}`)
    checked++
  }
  assert.ok(checked >= 2, 'Missing compiled frontend entry assets')
  console.log(`Using committed Fibersoft frontend (${checked} entry assets verified).`)
  console.log('To rebuild from source, run yarn build:frontend in the app directory.')
} catch (error) {
  console.error(`Invalid packaged frontend: ${error.message}`)
  console.error('Run yarn build:frontend and commit the generated assets before deploying.')
  process.exitCode = 1
}
