---
source: FPF-Spec.md
title: ### A.22.CGUS:10 - Rationale
level: 3
part: A
---
### A.22.CGUS:10 - Rationale

The selected design is a thin A.22 specialization of `U.Structure` because the recurring object is real but not a new root ontology. Constraint-based process modeling, case-management practice, artifact-centric modeling, acausal modeling, architecture-description practice, and FPF's own pattern use all separate a constraint-bearing structure from a performed trace, work order, view, publication, solver run, or example path. FPF adopts that separation as a constraint-governed unfolding structure and refuses to import one universal process calculus.

Physical modeling makes the same distinction concrete. In acausal modeling, component relations, quantities conserved across connections, and mode conditions can be declared before the model is compiled and solved in one chosen direction. The FPF import is only the general architecture of the move: structure and constraints first; derived calculation, demonstration, calibration, publication, or work use later under direct governing patterns.

CGUS is deliberately close to A.22. It is a `U.Structure` over a declared substrate in a bounded context. Descriptions, views, graph renderings, route cards, README entries, and examples help humans use it; they do not become it.

