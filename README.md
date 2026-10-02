# Practical workflows for ChatGPT and Codex

Three independent skills-only plugins by Kerry Morrison:

- **The Compiler** clarifies a request, produces a faithful executor prompt, checks results against the original goal, and proposes evidence-backed improvements.
- **GTM Engine** guides a builder through choosing reachable customers, shaping an offer, planning a bounded customer experiment, and reviewing reported outcomes.
- **Buyer / Target Book** turns authorized sources into a company brief or a ranked, evidence-linked account shortlist.

These packages do not run a hosted backend, collect analytics, send outreach, book appointments, or access accounts by themselves. Research depends on tools available to the user. Each workflow can also work from supplied material and labels what it cannot verify.

See [Privacy](docs/privacy.md), [Terms](docs/terms.md), and [Support](docs/support.md).

Source packages are under `plugins/`. Fictional acceptance cases and actual local walkthroughs are under `review/`. Run `python3 scripts/package.py` to validate and build separate upload ZIPs. ZIPs contain only plugin files, not this entire repository.
