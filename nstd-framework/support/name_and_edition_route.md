---
source: Narrativization-and-Narrative-Studies-Principles-Framework.md
title: ## Name And Edition Route
level: 2
---
## Name And Edition Route

Package name: `Narrativization and Narrative Studies Principles Framework`.

Public prefix for package pattern ids: `NSTD.*`.

`NSTD.*` is the package-local pattern prefix for this Domain Principle Framework. It is not an FPF Core id. The rejected `NAR.*` DPF prefix would collide with Core `A.6.3.NAR`.

```text
FrameworkEditionDependencyRecord@NarrativizationAndNarrativeStudiesPrinciplesFramework:
  frameworkEditionRef: NarrativizationAndNarrativeStudiesPrinciplesFramework@2026-06-30
  dependsOnEditionRefs: FPFCorePatternSet@current
  dependencyReason: DPF reuses FPF Core relation, source, coarsening, explanation, language-state, precision-restoration, ethics, evidence, assurance, quality, publication, generated-carrier, and refresh owners
  compatibilityBoundary: DPF may add domain patterns but may not redefine Core A.6.3.NAR, A.6.3.CSC, E.17.EFP, A.6.P, C.2.LS, A.16.1, A.16.2, C.16.Q, E.10, F.18, D.1 through D.5, A.10, B.3, A.19.ECS, C.16, or C.35
  deprecationOrSupersessionRefs: none for this package edition
  refreshConditionRefs: source-pack change, FPF Core edition change, failed teaching test run, generated-narrative SoTA change, evaluation-scale defect
  e53ConformanceNote: dependency points from this DPF toward FPF Core; Core has no reverse dependency
```

