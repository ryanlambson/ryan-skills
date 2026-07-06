# Ryan Skills

A Claude plugin marketplace (internal name: `ryan-skills`) holding Ryan Lambson's skills:
HTS liquor licensing, Green Holmes content, and shared utilities. One repo, version-controlled,
installable across devices.

## Plugins

| Plugin | Skills |
|---|---|
| `hts-lla-suite` | lla-gpt, lla-pia-drafter, lla-harm-minimisation, lla-citation-checker, lla-compliance-checker, lla-document-builder, lla-consumer-survey-drafter, lla-precedent-advisor, lla-new-project-setup, regulatory-fact-refresh, propagation-reminder, hts-small-bar-standards, lla-writing-conventions, lla-stakeholder-brief |
| `green-holmes-suite` | green-holmes-product, green-holmes-canva |
| `hts-utilities` | tracked-document-editor, surveymonkey-transposer, video-prompt-builder, skill-builder |

`green-holmes-publish` is intentionally NOT here — it carries a fal.ai key and a WordPress app
password, so it is kept inside Claude as a local personal skill only.

## Install in Claude

Settings → Plugins → ＋ → add `ryanlambson/ryan-skills` (or the full URL
`https://github.com/ryanlambson/ryan-skills.git`). Then install each of the three plugins.

## Updating

Edit a file, commit in GitHub Desktop, push. In Claude, remove and re-add the marketplace to
pull changes (this build has no in-place refresh).
