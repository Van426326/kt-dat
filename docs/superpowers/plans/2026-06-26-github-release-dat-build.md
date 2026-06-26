# GitHub Release DAT Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish `kt.dat` automatically through GitHub Actions.

**Architecture:** A single GitHub Actions workflow installs the official `v2fly/geoip` generator, uses the repository's existing `config.json` and `kt.txt`, verifies the generated output, and uploads it to a stable `latest` GitHub Release.

**Tech Stack:** GitHub Actions, Go, `github.com/v2fly/geoip`, `softprops/action-gh-release`.

## Global Constraints

- Use the repository files `kt.txt` and `config.json` as the source and generator configuration.
- Publish `kt.dat` through GitHub Release latest URL.
- Associate the local repository with `git@github.com:Van426326/kt-dat.git`.
- Do not commit generated `output/` artifacts.

---

### Task 1: Add CI Build And Release Workflow

**Files:**
- Create: `.github/workflows/build-dat.yml`
- Create: `.gitignore`

**Interfaces:**
- Consumes: `config.json`, `kt.txt`
- Produces: GitHub Release assets `kt.dat` and `kt.dat.sha256sum`

- [ ] **Step 1: Add workflow file**

Create `.github/workflows/build-dat.yml` with a push and manual trigger, Go setup, `v2fly/geoip` installation, generation, checksum, and release upload.

- [ ] **Step 2: Add generated output ignore rule**

Create `.gitignore` with `output/` so local generator output is not committed.

- [ ] **Step 3: Verify workflow structure locally**

Run: `git diff --check`

Expected: exit code `0`.

### Task 2: Initialize And Connect Repository

**Files:**
- Modify: `.git/config`

**Interfaces:**
- Consumes: local project files
- Produces: git repository connected to `git@github.com:Van426326/kt-dat.git`

- [ ] **Step 1: Initialize git if needed**

Run: `git init`

Expected: repository metadata is created in `.git`.

- [ ] **Step 2: Set default branch**

Run: `git branch -M main`

Expected: current branch is named `main`.

- [ ] **Step 3: Add remote**

Run: `git remote add origin git@github.com:Van426326/kt-dat.git`

Expected: `git remote -v` shows the `origin` fetch and push URL.

### Task 3: Verify Generator Behavior

**Files:**
- Read: `config.json`
- Read: `kt.txt`
- Generated locally, ignored: `output/dat/kt.dat`

**Interfaces:**
- Consumes: `config.json`, `kt.txt`
- Produces: local `output/dat/kt.dat` for verification only

- [ ] **Step 1: Install official generator**

Run: `go install github.com/v2fly/geoip@latest`

Expected: `geoip` command is available through Go's bin directory.

- [ ] **Step 2: Run generator**

Run: `geoip -c config.json`

Expected: `output/dat/kt.dat` exists and is non-empty.

- [ ] **Step 3: Verify generated artifact**

Run: `test -s output/dat/kt.dat`

Expected: exit code `0`.

### Task 4: Commit And Push

**Files:**
- Add: `.github/workflows/build-dat.yml`
- Add: `.gitignore`
- Add: `docs/superpowers/specs/2026-06-26-github-release-dat-build-design.md`
- Add: `docs/superpowers/plans/2026-06-26-github-release-dat-build.md`
- Add: `config.json`
- Add: `kt.txt`

**Interfaces:**
- Consumes: verified local repository state
- Produces: pushed repository that triggers GitHub Actions

- [ ] **Step 1: Check status**

Run: `git status --short`

Expected: intended files are staged or unstaged, and `output/` is ignored.

- [ ] **Step 2: Commit files**

Run: `git add . && git commit -m "feat: publish generated dat via github release"`

Expected: commit is created on `main`.

- [ ] **Step 3: Push to GitHub**

Run: `git push -u origin main`

Expected: branch is pushed and GitHub Actions starts the build.
