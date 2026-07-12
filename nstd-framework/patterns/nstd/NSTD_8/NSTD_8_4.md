---
source: Narrativization-and-Narrative-Studies-Principles-Framework.md
title: ### NSTD.8:4 - Solution
level: 3
---
### NSTD.8:4 - Solution

Create a learning route record and keep teaching materials outside pattern bodies.

```text
LearningNarrativeRoute@Context:
  learnerUse:
  sourceStructureSpineRefs:
  unfoldingStructureRefs?:
  demonstrativeSliceRefs?:
  sourceArchitectureRef?:
  learningRouteArchitectureRule:
  learningStepOrderingRule:
  interleavingPlanRefs?:
  spacingOrRetrievalScheduleRefs?:
  recurringAnchorRefs?:
  sourceReturnLinkRefs:
  learnerReconstructionTaskRefs:
  applicationTaskRefs?:
  engagementBoundaryRef?:
  narrativeRenderingQualityEvaluationRef:
  improvementLoopInputRef?:
  learningPublicationCarrierRefs:
  blockedTopicOverread?:
  nonAdmissibleUse:
  refreshCondition:
```

Actual lessons, seminar outlines, slides, exercises, scripts, session notes, recordings, and examples are separate teaching or test-run files. This pattern states how to design and evaluate them.

When the route teaches a constraint-governed unfolding structure, list that wider structure in `unfoldingStructureRefs?` and the taught path in `demonstrativeSliceRefs?`. The lesson may guide attention through one slice so learners can start working, but it must also teach what the slice omits and where the full structure is governed.

Build the route in eight design passes.

| Pass | Work product | Failure it prevents |
| --- | --- | --- |
| Source-spine pass | A short list of structures learners must later reconstruct or apply. | The lesson becomes an inspirational story or example chain. |
| Architecture-split pass | A split between source architecture and learning-route architecture. | The source module structure is copied as the course structure by default. |
| Ordering pass | A learning-step rule that may differ from monolith, proof, publication, or architecture order. | Learners confuse teaching order with source order. |
| Interleaving pass | Planned returns to earlier and neighboring source structures across sessions, examples, or exercises. | Learners learn each topic in isolation and cannot choose between similar owners later. |
| Spacing or retrieval pass | Delayed retrieval points for source-spine items, boundary cases, and repair moves. | Learners recognize material during the block but cannot retrieve it after delay. |
| Anchor pass | Repeated terms, diagrams, questions, or cases that return learners to the source spine. | Learners remember episodes but lose the framework. |
| Reconstruction pass | Tasks that ask learners to rebuild source structure, not only recall the narrative. | Satisfaction and memory replace practical competence. |
| Evaluation pass | `NSTD.6` rows for one route version and declared learner use. | Teaching tweaks are treated as improvement without evidence. |

Do not optimize the learning-route architecture for local neatness. A locally neat blocked route can be globally weak: it gives learners the answer key for the current block, so they do not practice selecting the right owner under mixed cues. Interleaving is useful when the learner must later discriminate similar patterns, methods, proof obligations, architecture structures, or source-return owners. Spacing is useful when the learner must still retrieve a structure after other material has intervened. Use them as design moves with declared learner use, not as decorative variety.

Use reconstruction tasks at several depths.

| Task depth | Example task | What it tests |
| --- | --- | --- |
| Recognition | "Which pattern owns this problem?" | Whether the learner can see the entry condition. |
| Reconstruction | "Rebuild the pattern-use route from source basis, forces, solution, and exit." | Whether source structure survived the narrative. |
| Transfer | "Apply the same route to a different domain case." | Whether the learner learned structure rather than anecdote. |
| Boundary | "Name the non-use condition and owner to return to." | Whether blocked overreads were retained. |
| Repair | "Given a low `NSTD.6` row, choose the smallest repair route." | Whether improvement discipline survived the lesson. |

The learning route may deliberately use examples, stories, rhythm, repetition, and analogy. Those devices are not defects. They become defects only when learners can no longer reconstruct the source spine or source-return boundary. A vivid example can be kept if the route also includes source-return markers and reconstruction tasks.

Telemetry does not have to be heavy. For a small route, it can be a short learner task result, a failed reconstruction note, or an observed confusion pattern. For a reliance-bearing or repeated course, telemetry should include route version, learner role, source spine covered, task result, repair action, and refresh condition. Do not describe this as evolution unless the route is treated as a holon across repeated operation and `B.4` is actually live.

If the route is improved across runs, first evaluate the concrete route version through `NSTD.6`. Use `E.22` when learner value, floor, protected trade-offs, evidence, or result form are still underframed; use `E.23` to repair a declared changed slice such as source spine, learning-step order, reconstruction tasks, learning publication carrier, engagement boundary, or evaluation characteristic space. Use `G.11` when source currentness, learner telemetry, teaching-test evidence, generated practice, or FPF edition changes; use `B.4` only when making an evolution claim about the learning route as a holon across repeated operation.

