import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
for (const folder of ['server', 'client']) {
  console.log(`\nBuilding ${folder}...`);
  const r = spawnSync(npm, ['run', 'build'], { cwd: join(process.cwd(), folder), stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status ?? 1);
}
console.log('\nBuild completed successfully.');
