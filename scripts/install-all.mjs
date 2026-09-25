import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
for (const folder of ['client', 'server']) {
  const dir = join(root, folder);
  if (!existsSync(join(dir, 'node_modules'))) {
    console.log(`\nInstalling ${folder} dependencies...`);
    const r = spawnSync(npm, ['install', '--no-audit', '--no-fund'], { cwd: dir, stdio: 'inherit', shell: false });
    if (r.status !== 0) process.exit(r.status ?? 1);
  }
}
console.log('\nAll dependencies are ready.');
