---
name: surveymonkey-transposer
description: >
  Deploys structured survey content into SurveyMonkey via the SurveyMonkey MCP
  connector. Use this skill whenever the user asks to push, transpose, deploy,
  build, or publish a survey to SurveyMonkey from existing structured content
  (markdown, .docx, or in-conversation drafts). Also trigger for requests to
  "put this in SurveyMonkey", "build the SurveyMonkey version", "create the
  survey in SurveyMonkey", "deploy to SurveyMonkey", or any instruction to
  move a finalised survey into the SurveyMonkey platform. Domain-agnostic —
  works for liquor licensing consumer surveys, research questionnaires,
  stakeholder feedback, or any other survey content destined for SurveyMonkey.
metadata:
  version: 1.0.0
  category: survey-deployment
  prerequisites:
    - SurveyMonkey MCP connector authorised in Claude
    - SurveyMonkey account on Advantage Annual plan or higher (API access required)
---

# SurveyMonkey Transposer

## Purpose

Deploys finalised, structured survey content into SurveyMonkey via the official
SurveyMonkey MCP connector. This skill handles the mechanical transposition only
— it assumes the survey content is already drafted, reviewed, and approved.

For survey content drafting (especially WA liquor licence consumer surveys),
defer to `lla-consumer-survey-drafter` first, then return here for deployment.

---

## Prerequisites

Before invoking this skill, confirm:

```
□ SurveyMonkey MCP connector is connected and authorised in Claude
□ User's SurveyMonkey account is on Advantage Annual or higher
  (Basic / Standard Monthly / Team Advantage do not expose API tokens —
   OAuth will succeed but tool calls return "missing_auth" errors)
□ Survey content is finalised (do not deploy works-in-progress)
□ User has confirmed the survey title and workspace destination
```

If the connector is registered but tool calls return `missing_auth`:
- The connection is in a half-state. Ask the user to fully **disconnect** and
  **reconnect** SurveyMonkey in their connectors settings, then retry.
- If that fails, check the SurveyMonkey plan tier.

---

## Order of operations

Deploy in this exact order. Skipping or reordering steps creates ID-tracking
problems and orphan elements.

### Step 1: Create the survey

```
create_survey(title: "<survey title>")
```

Returns:
- `id` — the survey ID, use for all subsequent calls
- `default_page_id` — the auto-created first page (page 1)

**Record both immediately.** All subsequent calls need the survey ID; the
default page ID is where the question content typically goes.

### Step 2: Get the page structure

```
get_pages(survey_id: <id>)
```

Confirms the default page exists and gives you its position. The default page
is position 1 — any intro pages will need to be inserted before it.

### Step 3: Add intro pages (if any)

For each intro page (e.g. Introduction, Manner of Trade, "What will happen with
the information you provide"):

```
add_page(
  survey_id: <id>,
  position: <1, 2, 3 ...>,
  page: { title: "<page title>", description: "<short description or empty>" }
)
```

Use `position` to insert intro pages **before** the default questions page.
Adding three intro pages at positions 1, 2, 3 pushes the default questions
page to position 4.

Record each new page ID — you'll need them in Step 4.

### Step 4: Add descriptive text blocks for intro content

The intro text itself goes inside a `presentation/descriptive_text` question on
each intro page. SurveyMonkey does **not** have a native page-level "text only"
element — descriptive_text questions are the closest equivalent.

```
add_question(
  survey_id: <id>,
  page_id: <intro page ID>,
  position: 0,
  question: {
    family: "presentation",
    subtype: "descriptive_text",
    headings: [{ heading: "<full text content>" }]
  }
)
```

Notes:
- The `heading` field accepts plain text with `\n` for line breaks and `\u2022` for bullet markers
- HTML is not rendered in descriptive_text — use Unicode bullets instead
- No answer choices needed

### Step 5: Add survey questions

Build each question on the designated questions page (typically the
default page from Step 1). Add questions in **reverse order** if using
`position: 0`, or use sequential positions.

Common question type → family/subtype combinations:

| Question type | family | subtype |
|---------------|--------|---------|
| Single-select (radio) | `single_choice` | `vertical` |
| Multi-select (checkboxes) | `multiple_choice` | `vertical` |
| Free text (multi-line) | `open_ended` | `essay` |
| Free text (single line) | `open_ended` | `single` |
| Dropdown | `single_choice` | `menu` |
| Contact info | `demographic` | `international` (or `us` for US-only forms) |
| Date | `datetime` | `date_only` |
| Rating scale | `matrix` | `rating` |
| Descriptive text | `presentation` | `descriptive_text` |

Use `get_question_types()` if uncertain — it returns the full enumeration.

### Step 6: Create the web link collector

```
create_weblink_collector(survey_id: <id>, name: "<collector name>")
```

This generates the public shareable URL. The user will be prompted to approve
this action — it's a permission gate, not an error.

### Step 7: Hand off the manual configuration list

The MCP server does not expose every SurveyMonkey feature. The user must
manually configure the remaining items in the SurveyMonkey UI (see "Known
limitations" below).

---

## Question schemas — the gotchas

### Single-select and multi-select (straightforward)

```json
{
  "family": "single_choice",
  "subtype": "vertical",
  "headings": [{ "heading": "<question text>" }],
  "answers": {
    "choices": [
      { "text": "Option 1" },
      { "text": "Option 2" }
    ]
  }
}
```

Multi-select uses `family: "multiple_choice"` — everything else is identical.

### Contact information (the schema trap)

The `demographic/international` question type requires **exactly 10 choices**
in a **fixed order**, with `type`, `visible`, and `required` flags on each. The
schema does **not** accept partial lists or rows.

Required choice types in order:
1. `name`
2. `company`
3. `address`
4. `address2`
5. `city`
6. `state`
7. `zip`
8. `country`
9. `email`
10. `phone`

Hide the fields you don't want by setting `visible: false`. Standard pattern
for a name + suburb + email + phone block:

```json
{
  "family": "demographic",
  "subtype": "international",
  "headings": [{ "heading": "<heading + 18+ declaration if applicable>" }],
  "answers": {
    "choices": [
      { "type": "name", "text": "Name", "visible": true, "required": true },
      { "type": "company", "text": "Company", "visible": false, "required": false },
      { "type": "address", "text": "Address", "visible": false, "required": false },
      { "type": "address2", "text": "Address 2", "visible": false, "required": false },
      { "type": "city", "text": "Suburb", "visible": true, "required": true },
      { "type": "state", "text": "State", "visible": false, "required": false },
      { "type": "zip", "text": "Postcode", "visible": false, "required": false },
      { "type": "country", "text": "Country", "visible": false, "required": false },
      { "type": "email", "text": "Email Address (Optional)", "visible": true, "required": false },
      { "type": "phone", "text": "Phone Number (Optional)", "visible": true, "required": false }
    ]
  }
}
```

Note that `text` relabels the field in the respondent UI — use this to
rename "City/Town" to "Suburb" for Australian respondents.

### Descriptive text (presentation)

No `answers` block — just `headings`:

```json
{
  "family": "presentation",
  "subtype": "descriptive_text",
  "headings": [{ "heading": "<text content with \\n line breaks>" }]
}
```

---

## Known limitations and workarounds

The SurveyMonkey MCP server does not expose every feature of the SurveyMonkey
platform. Plan around these gaps from the start.

### No skip-logic API

`Question Skip Logic` cannot be configured via MCP. Workarounds:

- **Include the routing hint in answer text** (e.g. "Yes (Go to Q9)") so respondents see the intended flow even if the logic isn't enforced
- **Hand off to the user** with a clear instruction: "Configure Q[X] skip logic in the SurveyMonkey UI: Question → Logic → Question Skip Logic. Set: [rules]."

Recommended hand-off template:

> In the SurveyMonkey editor, open Q9 ("Do you support the liquor store
> licence application…") → click **Logic** → **Question Skip Logic** →
> set: Yes → skip to Q11; No → continue to Q10; Unsure → skip to Q11.

### No image upload

`add_question` does not accept image attachments, even for the
`presentation/image` question type. Workarounds:

- **User uploads images manually** in the SurveyMonkey UI after deployment
- **Leave a placeholder note** in the page description or descriptive_text:
  "[Image to be inserted: <description>]"

### No collector customisation

`create_weblink_collector` returns a default-configured collector. Custom
thank-you pages, branding, response limits, and password protection must be
configured manually in the SurveyMonkey UI.

### No question reordering

There is no `reorder_questions` tool. To reorder, you must delete and re-add
questions in the desired order, which loses any response data. Plan question
order before deployment.

### Approval prompts on certain actions

`create_weblink_collector` triggers a permission prompt. The user must tap
**Allow** before the collector is created. This is not an error — it's the
permission gate. If you see "No approval received" in the tool result, ask
the user to approve and retry.

---

## Standard hand-off message

At the end of every deployment, give the user this hand-off:

```
Survey deployed to SurveyMonkey.

Survey ID: <id>
Edit link: https://www.surveymonkey.com/create/?sm=<id>
Public link: <weblink collector URL>

Manual configuration required:

1. [If skip logic applies] Configure Q[X] skip logic:
   Survey → Logic → Question Skip Logic on Q[X] → set [rules]

2. [If images apply] Upload images to:
   Page <N>: <description>

3. Preview the survey end-to-end on desktop and mobile.
4. Test the skip logic by submitting test responses for each [Yes/No/Unsure].
5. Generate the QR code for the printed PDF version (if cross-channel distribution).
```

---

## Workflow examples

### Example 1: Liquor licensing consumer survey

```
1. lla-consumer-survey-drafter produces final markdown
2. User approves the markdown
3. User invokes surveymonkey-transposer
4. Transposer creates survey
5. Transposer adds 3 intro pages (Introduction, Manner of Trade, What will happen)
6. Transposer adds descriptive_text blocks on each intro page
7. Transposer adds 14–16 questions on the default questions page
8. Transposer requests collector approval, creates weblink
9. Hand-off message includes Q9 skip-logic configuration instruction
```

### Example 2: Stakeholder feedback survey

```
1. User provides survey content directly (no LLA context)
2. Transposer creates survey with single-page or multi-page structure as specified
3. Transposer adds questions
4. Transposer creates collector
5. Hand-off message lists any manual steps
```

---

## Common errors and fixes

| Error | Likely cause | Fix |
|-------|--------------|-----|
| `missing_auth` | Connector not fully authorised | Ask user to disconnect + reconnect SurveyMonkey |
| `missing_auth` (persistent) | SurveyMonkey plan tier insufficient | Confirm Advantage Annual or higher |
| `Family/subtype combination does not exist` | Wrong family/subtype pairing | Call `get_question_types()` to verify |
| `Additional properties are not allowed` | Schema mismatch (e.g. `rows` instead of `choices`) | Check the schema for that specific family — demographic uses `choices`, matrix uses `rows` |
| `No approval received` | Permission prompt triggered | Ask user to tap "Allow" and retry the same call |

---

## Lessons captured

- **Thirsty Camel Witchcliffe (May 2026):** First end-to-end MCP deployment.
  Discovered the contact-info schema requires exactly 10 ordered choices, not
  the more intuitive rows-array. Discovered descriptive_text as the workaround
  for native page-text blocks. Confirmed no skip-logic API.

Future lessons should be added to this section as they emerge.
