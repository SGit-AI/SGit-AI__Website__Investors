---
title: Release history
description: Every release of the site, numbered by CI and read from the repository's tags on every build.
status: live
---
# Release history

Every push to `dev` that passes the gate is a release, numbered by CI: the last number goes up. A merge from `dev` to `main` bumps the middle number. No person and no agent types a version number. This list is read from the repository's tags when the site is built.

This build is **{{ version }}**.

{{ releases.list }}
