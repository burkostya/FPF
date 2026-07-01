---
source: FPF-Spec.md
title: ### A.6.P:7a - Portfolio, front, archive, and shortlist disambiguation
level: 3
part: A
---
### A.6.P:7a - Portfolio, front, archive, and shortlist disambiguation

- Treat bare uses of `portfolio`, `front`, `archive`, `Pareto`, `shortlist`, `space`, `reachability`, and `stepping stone` as repair triggers whenever they carry live explanatory work.
- Use the helper declarations from A.0:QF.1a when repairing the sentence: do not let `SetResultFamily`, `SourceSetFamily`, `SourceSetComposition`, `SubjectKind`, `DerivedViewKind`, `BasePaletteRef`, `SelectorOutcomeKind`, `HandoffKind`, `PromotionPolicy`, `RetentionIntent=steppingStone`, `EligibilitySet`, `DominanceSet`, `TieBreakerSet`, or `TelemetrySet` read as public set-outcome heads.
- The minimum repair is to state the `SubjectKind`, the declared comparison bundle, and, when selection or publication outcomes are involved, the declared `SelectorOutcomeKind`, the applicable `SetResultFamily` or `HandoffKind`, the declared `SourceSetFamily`, `SourceSetComposition` when several sources are actually composed, `DerivedViewKind` or `BasePaletteRef` when a derived palette view matters, `LensId`, and which member of the shortlist family is meant.
- The declared comparison bundle is:
  - `EligibilitySet`
  - `DominanceSet`
  - `TieBreakerSet`
  - `TelemetrySet`
- If one front sentence depends on current `Q`, say whether the `DominanceSet` is the declared `Q` components or one promoted bundle under explicit policy.
- If one archive claim depends on coverage, stepping-stone retention, or reachability rather than current dominance, state that archive purpose explicitly instead of borrowing `Front` language.
- If one phrase uses `SoTA portfolio` before comparison or choice semantics exist, rewrite it as `TraditionPalette` only when the members are traditions; otherwise rewrite it as `Palette + SubjectKind`.
- If one phrase uses `Pareto archive` for the whole retained exploration outcome, rewrite it as `ExplorationArchive`.
- If one phrase uses `stepping-stone set` for the whole retained exploration outcome, rewrite it as `ExplorationArchive` and reserve `SteppingStoneSet` for one narrower retained subset when that narrower retention requirement really matters.
- If one selected set is mentioned, name the shortlist-family stack explicitly:
  - `Shortlist` for the selected outcome
  - `RankedShortlist` for its ordered specialization
  - `ShortlistId` for the emitted identity or public token
  - `ChoiceSet` only when the mathematical set object itself is the point of the sentence
- If one phrase says `choice set` but the sentence is naming the public selected outcome, rewrite it as `Shortlist` and keep `choice set` only as one mathematical gloss when needed.
- If one phrase says `shortlist` and the output is explicitly ordered, rewrite it as `RankedShortlist` and keep it distinct from `Shortlist`.
- If one phrase says `shortlist` but really points at one emitted token or publication handle, rewrite it as `ShortlistId`.
- If one sentence moves between search-space and outcome-space talk, name the space whose objects are being compared before making claims about dominance, archive retention, or frontier expansion.
- If one sentence says `Pareto` but really means one post-lens selected result, rewrite it as `Shortlist` or `RankedShortlist` rather than widening `Front` until it means everything.
- Canonical rewrites for FPF-governed Q-Front / NQD prose:
  - `portfolio by Q` -> `Front over the declared Q components` when the sentence is about non-domination.
  - `portfolio by NQD` -> `Front over the declared DominanceSet plus ExplorationArchive under the declared retention policy` when both current front and retained exploration outcome are meant.
  - `Pareto shortlist` -> `Shortlist from <SourceSetFamily> under <LensId>` when the sentence is about publication or selection.
  - `Pareto archive` -> `ExplorationArchive under <RetentionPolicy>` when the sentence is about retained exploration rather than current non-domination.
  - `space of traditions, methods, and hypotheses` -> `Palette + SubjectKind` first; add `TraditionPalette` only for `SubjectKind=Tradition`.
- Discriminating tests:
  - If the sentence answers "what counts as current non-domination?", repair toward `Front` / `Q-Front` plus `DominanceSet`.
  - If the sentence answers "what remains worth retaining for reach, coverage, or later probing?", repair toward `Archive`, `ExplorationArchive`, or `RetentionIntent=steppingStone`.
  - If the sentence answers "what selected set was emitted for downstream use?", repair toward `Shortlist`, `RankedShortlist`, and optional `ShortlistId`.
  - If the sentence answers "which goal, capability, or learning frontier might widen next?", repair toward `GoalSpaceExpansionCue`, `LearningProgressSignal`, or `CompetenceModelRef`, and keep those outside default dominance unless one policy promotes them.

