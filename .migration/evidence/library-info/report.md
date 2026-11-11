# Slice library-info — acceptance evidence

- Tickets: LL-04 (#65), LI-AUDIT (#122) · Commit: `7d4b249e342a94e7176ebf3e1d370f81d7156b16` · Date: 2026-11-11
- Acceptance run: [42938753426, attempt 1](https://github.com/martins-vds/ai-factory-synthetic-target/actions/runs/42938753426); artifact `afs-acceptance-7d4b249e342a94e7176ebf3e1d370f81d7156b16-42938753426-1`
- Verified archive: `.migration/evidence/acceptance-runs/42938753426-1.json`

## Verification and graph

Fetched and verified the run through `afs-run`. The archive identifies repository `martins-vds/ai-factory-synthetic-target`, attempt 1, the exact commit above, and a passed result. GitHub reports successful `graph / understand`, `acceptance`, and `publish` jobs. The archive's target graph was built for the same commit and passed its ownership-enforced gate. Its report lists 27 entry points, 18 reaching data, and explicitly lists both `GET /about` and `GET /ui/about/` as having no data path. These static information routes are correctly non-data flows, not missing ledger data paths. The artifact expires 2026-12-11.

The source graph was fresh and its gate passed in this audit. Relevant target paths, the slice spec, plan, ledger, characterization golden, and LL-04 evidence have no changes between the acceptance commit and the audited checkout.

## Gates

Acceptance gates were not rerun by the Auditor; this table reflects only the independently fetched, verified run. The acceptance journal rows were appended unchanged to `.migration/evidence/runs/LI-AUDIT.md`.

| Gate | Command | Exit | Notes |
|---|---|---:|---|
| Runtime, harness integrity, services | `check_runtime.py`; `check_installed.py`; `afs-services check` | 0 | All passed. |
| Graph freshness and source graph | `check_graph_fresh.py --require source,target`; `graph_gate.py --side source --require-graph` | 0 | Source graph also independently checked in this audit. |
| Target graph | `graph_gate.py --side target --require-graph --enforce-ownership` | 0 | 27 entry points; 18 reach data; both About routes have no data path. |
| Build | `python -m compileall -q src`; `python manage.py check` | 0 | Both passed. |
| Idiom | `ruff check src config manage.py tests`; `ruff format --check src config manage.py tests` | 0 | Both passed. |
| Tests | `pytest -q` | 0 | Full suite passed. |
| CRAP | `crap.py ... --max 30` | 0 | Maximum 7.0; threshold 30. |
| Full mutation | `afs-mutation --all` | 0 | Score 0.976; threshold 0.8; 244 killed, 6 survived, base `all`. |

## Characterization and capability coverage

The single capability in `.migration/slices/library-info.yaml` is `about.page`. Its ledger entry names existing routes, views, templates, the tier-A HTTP/browser goldens, and executable boundary tests.

- `GET /about`: the source golden specifies HTTP 200, `text/html`, and exact static HTML. The target's `/about` test compares status, content type, and decoded body against that golden; the LL-04 differential record reports a byte-for-byte match. This preserves the characterized route.
- `GET /ui/about/`: this is an approved target addition, separate from the legacy/API path. The approved `reading-room` decision (#38, #50) and slice plan require the modern page. The browser test checks its heading, description, opening hours, 14-day term, `mailto:` contact, and Loans navigation; the template inherits the approved daisyUI/Tailwind/htmx base assets. Both routes reject non-GET requests in the executable tests.
- Test-first evidence: the LL-04 journal records failing `red-about-legacy` and `red-ui-about` runs before their passing targeted runs. Earlier full-suite isolation and mutation blockers are recorded in verifier issue #104 / PR #105; the re-verification issue #113 / PR #115 records the fix and passing gates. The acceptance run's full `pytest -q` also passed.
- Quirks #39–#43 cited by LL-04 are explicitly ruled `fix` in the decision map. They concern loan-field validation, payment interruption, repeated returns, persistence, and export; none changes the public About page behavior or its routes.

| Capability | Target components | Evidence and result |
|---|---|---|
| `about.page` | `config.urls.urlpatterns`; `src.library_info.urls`; `src.library_info.views.about` and `about_page`; `legacy_about.html`; `about.html` | Tier-A golden comparison and executable HTTP/browser tests; full acceptance tests pass. No missing component, broken flow, integration gap, or review-only capability found. |

## Mutation survivors

The six full-run survivors in `.migration/runs/acceptance-42938753426-1/mutants.md` affect loan catalog templates/context, loan URL routing, fee dataclass mutability, and loan form metadata. None touches library-info. LL-04's own last mutation record reports score 1.000, 8 killed, 0 survived (`.migration/evidence/mutants/LL-04.md`); its final verifier return is `pass`.

## Human check

Independent Auditor review completed 2026-11-11: one capability checked, no gaps, no graph inconsistencies. **Audit verdict: complete.** The operator's human flow sign-off remains the Slice Coordinator's subsequent step; this report does not represent that sign-off.
