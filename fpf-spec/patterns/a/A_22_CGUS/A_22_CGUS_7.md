---
source: FPF-Spec.md
title: ### A.22.CGUS:7 - Conformance Checklist
level: 3
part: A
---
### A.22.CGUS:7 - Conformance Checklist

| ID | Passing condition | Failed-check repair |
| --- | --- | --- |
| **CC-CGUS-1 Structure kind.** | The object is `ConstraintGovernedUnfoldingStructure@Context <: U.Structure` or a named narrower `U.Structure` specialization. | Lower to note, seed, description, route card, method description, or governing-pattern record. |
| **CC-CGUS-2 Typed positions and cross-position constraints.** | More than one SlotSpec-grounded position is named, and exact relations or constraints among those positions affect admissible continuations. | Add typed positions and their exact relation references, or stop using CGUS. |
| **CC-CGUS-3 Description separation.** | A pre-admission presentation remains a `ProvisionalUnfoldingDemonstrationDescription@Context`; after admission, a whole-structure account is a `ConstraintGovernedUnfoldingStructureDescription@Context`, while one selected traversal is a `DemonstrativeUnfoldingSlice@Context` whose EntityOfConcern is the admitted CGUS. | Keep the presentation provisional until CGUS admission. After admission, choose the description species by whether the episteme describes the admitted topology or selects one traversal through it. |
| **CC-CGUS-4 Direct governing patterns.** | Method, work, evidence, gate, decision, architecture, publication, refresh, and mathematical claims point to direct governing patterns. | Add governing-pattern exits or narrow the claim. |
| **CC-CGUS-5 Non-workflow boundary.** | The structure does not prescribe performed-work order by itself. | Move work-order claims to a work plan or method description if justified. |
| **CC-CGUS-6 Admissible next form.** | At least one admissible next-form kind is named for the admitted structure. | Keep the artifact as a provisional description until a next use and next-form kind are recoverable. |
| **CC-CGUS-7 Stop, return, and currentness reference.** | Stop and return boundaries are recoverable; any currentness claim is an exact referenced relation governed by `G.11`. | Add the boundary or referenced currentness relation, or lower the structure to a one-use explanation. |
| **CC-CGUS-8 Graph-shaped structure coverage.** | If the admitted starting record set, starting structure set, or visible expression is graph-shaped, case-like, or workflow-shaped, branching, joining, cyclic, partial-order, and alternative-live-next-form structure is preserved or explicitly lost. | Do not collapse the object to a chain. Keep the chain provisional before admission, or make it an admitted slice afterward and name the omitted graph structure. |

