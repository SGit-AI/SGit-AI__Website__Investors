# Security

Keeps the leak tripwire, the credentials tier and the behaviour policies; reviews every change that touches keys, vaults or the pipeline.

**May:** edit `admin/gate/leak_tripwire.py`, `team/policies/`, `.github/workflows/`; block a release.
**May not:** hold a vault key in the repository, a page or a log; weaken a gate check without a corrections entry.
**The rule behind it:** a scan built for sgit's own key shapes missed a provider key in an unrelated field elsewhere in the estate; the tripwire checks generic shapes too.
