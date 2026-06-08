# Example 2 — MCP Enhancement Skill

A skill that orchestrates an existing MCP connector. Adds workflow expertise on top
of raw tool access. Multiple scripts.

## Brief (Phase 1)

**Skill name:** `publishing-greenholmes-wordpress-posts` (verb-ing pattern; longer name is OK if under 64 chars)
**Trigger phrases:**
- "Publish this to Green Holmes"
- "Post to greenholmes.com.au"
- "Push this to WordPress with a featured image"
- "Launch the post on staging"
- "Schedule this for Green Holmes"

**Negative triggers:** Do not trigger for non-Green Holmes WordPress sites. Do not
trigger for social posts (use `green-holmes-social` skill instead).

**Core workflow:**
1. Parse the post content from chat or attached file
2. Generate a brand-locked featured image via FLUX (fal.ai API)
3. Upload the image to WordPress media library
4. Create or update the post with the image attached
5. Set categories, tags, and SEO fields
6. Return the staging URL and publish-ready confirmation

**Gates:** Do not publish without explicit Ryan approval of the staging URL. Refuse
to publish directly to production — staging-first is non-negotiable.

**Authority hierarchy:**
1. Green Holmes brand voice (`green-holmes-voice` skill if loaded) wins on copy
2. `green-holmes-brand-qa` rules win on visual standards
3. This skill's workflow wins on publishing mechanics

**Output type:** Published post on staging, plus URL returned to chat.

**Bundled scripts:**
- `generate_featured_image.py` — calls fal.ai FLUX API with brand-locked prompt
- `upload_to_wordpress.py` — REST API call to staging.greenholmes.com.au
- `validate_post.py` — runs the publish-ready checks (alt text, meta description, categories)

**MCP / tool dependencies:** WordPress REST API (custom), fal.ai API. No off-the-shelf
MCP — direct HTTP calls.

**Distribution target:** Claude.ai only (relies on Anthropic-environment networking).

## Research (Phase 2)

- Tier 1: Internal knowledge of REST APIs and Green Holmes brand standards
- Tier 2: Drive `green-holmes-publish` folder — check existing implementation
- Tier 3: Scrape fal.ai docs (https://fal.ai/models/fal-ai/flux-pro) for current API,
  scrape WordPress REST API docs for staging.greenholmes.com.au

## Outline (Phase 3)

```
publishing-greenholmes-wordpress-posts/
├── SKILL.md  (~250 lines)
├── scripts/
│   ├── generate_featured_image.py
│   ├── upload_to_wordpress.py
│   └── validate_post.py
├── references/
│   ├── brand-image-prompts.md  (prompt templates for FLUX)
│   └── wp-api-fields.md         (field reference for the WP REST endpoints)
└── assets/
    └── default-categories.json
```

## Draft (Phase 4)

SKILL.md focuses on workflow orchestration. Detailed prompt engineering for FLUX
sits in `references/brand-image-prompts.md`, loaded only when the image-gen step runs.

QA gate flags one issue: `validate_post.py` originally hardcoded the staging URL.
Fixed to read from environment variable. Gate re-runs and passes.

## Output

`/mnt/user-data/outputs/publishing-greenholmes-wordpress-posts.zip` + Drive backup at
`SKILLS/publishing-greenholmes-wordpress-posts/`.

---

**Why this is a useful example:**

Shows the MCP-enhancement / API-orchestration pattern. SKILL.md is the workflow;
scripts are the deterministic execution; references are the deep detail; assets are
the config. Authority hierarchy resolves conflicts with other Green Holmes skills.
Hard gate (staging-first) is encoded in the workflow, not relied on language.
