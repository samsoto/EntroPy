<!-- yaiml-revision: 0.1.46b565251e398e76 -->
# EntroPy project guidance

Preserve Sam's original information-theory and time-series exploration. The
user wants to make this old repository useful and approachable, with corrected
calculations, clear graphics, and a light browser UI. Distinguish that human
direction from inferred details of Sam's original intent; there is no separate
approved roadmap from Sam in this checkout.

The UI calls the existing Python audit. Keep mathematical behavior in Python;
do not invent browser-only scores or duplicate the estimator in JavaScript.
The workbench runs locally. The user authorized packaging this enhancement on
`feature/jw-1`, pushing it, and opening a pull request for Sam, with clear local
run instructions. A fork is appropriate when upstream write access is absent.
This does not authorize merging, hosted deployment, or automatic backlog work.
Preserve unrelated work. Branch creation alone does not commit files.

## UI and visual design

The user strongly dislikes repetitive AI-generated interfaces, especially dark
navy backgrounds, teal accents, rounded bordered cards, pill badges, and the
same generic dashboard composition. Treat this as a standing design requirement.

- For each new UI or substantial redesign, choose a distinct visual direction
  suited to the product, its content, and its users. Do not reuse the same
  dashboard shell and merely change labels or accent colors.
- Inspect concrete, varied design references before implementation. HTML5 UP
  and Framer Marketplace are useful starting points, not mandatory platforms or
  a fixed house style. Respect licenses when reusing assets or code.
- Avoid the dark-navy/teal/rounded-card combination unless explicitly requested.
  Do not wrap every section in a card or default to pill-shaped controls.
- Make meaningful choices in layout, typography, spacing, density, imagery,
  color, and shape. Editorial, Swiss typographic, industrial, or playful styles
  are options, not universal defaults.
- Own routine design decisions. Briefly identify the direction and proceed;
  avoid questionnaires and repeated approvals. Requested options must differ
  in structure as well as color.
- Preserve usability, accessible contrast, focus states, and responsive behavior.
- Existing generated styling is not approval. Improve affected screens coherently
  within scope; preserve explicitly approved identities and references. Backend
  fixes alone do not require redesign.
- Inspect the rendered UI before delivery. Revise rejected aesthetics rather
  than describing them as unique. Never claim visual checks that were not run.

## YAIML Context And Skills

Read and follow `.yaiml/YAIML_GUIDE.md` for ordinary work, using
`.yaiml/yaiml.yml` to locate project memory. Reuse current context; select
specialized methods from host metadata or `.yaiml/skills/INDEX.md` only when
needed. Preserve user arguments and project authority.

Before finishing, maintain material understanding and revision/change records
as the guide directs, including confirmed conversational decisions. Respect
read-only scope and no-op work. At startup/context refresh consider coordination
without extra scans; only for a concrete benefit read `.yaiml/YAIMLACP.md` and
obtain its scoped affirmative confirmation before use. No delegation is
authorized by this setup.
