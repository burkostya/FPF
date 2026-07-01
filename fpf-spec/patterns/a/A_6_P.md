---
source: FPF-Spec.md
id: A_6_P
title: ## A.6.P — Relational Precision Restoration (RPR) — Kind‑Explicit Qualified Relation Discipline
part: A
level: 2
parent: A
---
## A.6.P — Relational Precision Restoration (RPR) — Kind‑Explicit Qualified Relation Discipline

> **Type:** Architectural (A)
> **Status:** Stable
> **Normativity:** Normative (Core)

**Plain-name.** Relational precision restoration.

**Intent.** Provide a reusable governing discipline for repairing a recurring defect in FPF texts: **under-specified relational language** (often phrased as a seemingly binary verb) that actually hides **(i)** higher arity (missing participant positions), **(ii)** multiple semantic change classes, **(iii)** asymmetry between `U.Viewpoint` specifications and `U.View` instances, **(iv)** boundary requirements such as signature invariants, admissibility, deontics, evidence, or work, and **(v)** endpoint referential compression through pronominal stand-ins, metonymic stand-ins, or over-broad kinds.
RPR patterns turn “umbrella relations” into **kind‑explicit, slot‑explicit, qualified relation records** with an explicit **change-class lexicon** and **lexical guardrails**, while respecting the **A.6 Signature Stack** and **A.6.B Boundary Norm Square** separation.

**Use this when.** Use `A.6.P` when wording hides a relation-bearing use: sameness, linkage, grounding, support, basedness, mapping, comparison, dependency, whole or part, service, cross-context bridge wording, endpoint compression, qualifier-carried claim, or another relation-bearing phrase that must be used for FPF guidance, publication, comparison, gating, assurance, decision, or reuse.

**What goes wrong if missed.** An umbrella verb or noun starts acting like a relation ontology: endpoints, slot kinds, direction, scope, time, admissible use, and neighboring governing patterns disappear behind a familiar phrase.

**What this buys.** The relation becomes reviewable: head kind, endpoints, slots, qualifiers, scope, time, viewpoint, admissible use, non-admissible overread, and relation record are made explicit enough for the neighboring FPF pattern governing that claim to compose with it.

**First useful move.** Restore the head kind and the relation or comparison use separately. If the problem is only source-expression, publication, architecture or structure, characteristic or scale, quality characterization, evaluative characterization, or function-like kind recovery, use the pattern governing the recovered claim named below instead of forcing relation repair.

**Not this pattern when.** Do not use `A.6.P` as a universal wording-repair pattern, evidence pattern, assurance pattern, quality pattern, source-use pattern, or architecture pattern. If `E.10` already recovered the pattern governing the recovered claim, kind, or relation, use that governing pattern directly.

**Placement.** Part A → cluster **A.6 Signature Stack & Boundary Discipline** → governing pattern for **RPR specialisations** (A.6.5, A.6.6, A.6.8, A.6.9, A.6.H, and any additional A.6.x pattern that declares this RPR relation).

**Builds on.**

* **A.6** (stack layering + boundary discipline requirements).
* **A.6.B `U.BoundaryNormSquare`** (L, A, D, and E classification; claim atomicity; cross-quadrant references).
* **A.6.S `U.SignatureEngineeringPair`** (TargetSignature vs ConstructorSignature; canonical constructor verb mapping; effect‑free constructor ops).
* **A.6.0 `U.Signature`** (SlotSpec requirement for argument positions).
* **A.6.5 `U.RelationSlotDiscipline`** (SlotKind, ValueKind, and RefKind stratification + canonical slot verbs; `bind` reserved for name binding).
* **A.6.RSIR** (interface cue, signature, role, slot, and relation precision restoration; selects the governing interface-like case before generic RPR is allowed).

* **E.8** (pattern authoring discipline; Tell–Show–Show; SoTA echoing hygiene).
* **F.18** (local-first reusable naming after relation kind and use recovery: minting decisions, reuse decisions, externally fixed name documentation decisions, collision checks, lineage notes, and durable-name discipline).
* **E.10** (LEX‑BUNDLE discipline; EntityOfConcern versus Description epistemes and specification-use cases plus publication face, form, unit, carrier, and rendering discipline; publication-face or publication-form token discipline; reserved primitives; Tech↔Plain pairing). *(Referenced conceptually; no extra authoring apparatus implied.)*

**Coordinates with.**

* **A.10, B.3, F.10, and E.17 evidence, status, and source-use discipline** (carrier-referenced evidence use, assurance use, status-source use, publication use, timespan, and freshness when decision-relevant).
* **A.2.6 scope + `Γ_time` discipline** (avoid implicit “current” or “latest”; make time selectors explicit when time matters).
* **A.7 Strict Distinction** (EntityOfConcern, Description episteme, specification use, publication face, form, unit, carrier, and rendering; avoid treating evidence or logs as properties of prose).
* **A.6.2–A.6.4** (effect‑free episteme morphisms, epistemic viewing and retargeting as disciplined slot writes).
* **A.10 evidence discipline** (witnesses are carrier-referenced; freshness is adjudicated in work and evidence relations).
* **C.2.1 `U.EpistemeSlotRelation`** (slot read and write profiles for constructor operators, when declared).
* **C.3.3 `U.KindBridge` + `CL^k` discipline** (repairing endpoint kind mismatches; kind-level congruence + loss notes).
* **E.17 MVPK and multi-view publication** (faces are views; "no new semantics"; viewpoint accountability).

* **F.17 `UTS`** (when ambiguity clusters become recurring vocabulary: publish stable `RelationKind` tokens and facet head phrases as UTS and LEX-UTS term assets, so rewrites do not live only inside A-patterns).
* **F.9 Bridges + CL** for cross-Context or cross-plane reuse (no silent sameness).
* **C.2.2a, A.16, A.16.1, A.16.2, B.4.1, and B.5.2.0** for the language-state boundary: language-state chart positions, admissible moves, pre-threshold cue preservation, next-pattern publication, admissible retreat or reopen, and prompt-shaped continuations that are not yet stable relation publication; use **A.16.0** only when lineage, branch, loss, or responsibility-transfer history itself must be published as an explicit trajectory account.
* **C.2.LS, C.2.4, C.2.5, C.2.6, and C.2.7** for language-state facet governance: articulation explicitness, closure degree, language-state anchoring mode, and the language-state representation-factor bundle may be cited by RPR patterns but are not governed here.

**Specialisations already in Core.**
These retained specialisations are current because they each carry one stable recurring repair case. Their mnemonic heads remain admissible entry points, but generic `A.6.P` does **not** treat token recurrence alone as sufficient to mint one new specialisation per overloaded trigger word.

* **A.6.5**: RPR for n-ary relations and slot discipline (archetype: "putting something into a place"; explicit SlotKinds, ValueKind, RefKind, and slot-operation lexicon).
* **A.6.6**: RPR for relative-to and basedness claims (explicit `baseRelation` token, scoped witnessed base declarations, and base-change lexicon; lexical red-flags for `anchor*`; support-as-basedness selection test for `support`, `supported by`, `support basis`, and `support relation` wording).
* **A.6.8 (RPR-SERV)**: RPR for the "service" cluster polysemy (facet-explicit `serviceSituation` lens; canonical rewrites for `service`, `server`, and `service provider`; classification tests for clause, access point, provider commitment, work, and evidence).
* **A.6.9 (RPR-XCTX)**: RPR for cross-Context "same", "equivalent", "align", or "map" talk (explicit Bridges with direction, endpoint refinement, substitution licence, CL, and loss notes; blocks silent inversion and "alignment" umbrella verbs).
* **A.6.H (RPR-WHOLE)**: RPR for "whole", "part", "integrity", and "complete" polysemy (WHOL triggers plus Boundary-Parthood-Fold-Order-Time-Completeness lens; maps turnkey and end-to-end wording into A.15 coverage; includes publication-form, referent, and work-level tests).

