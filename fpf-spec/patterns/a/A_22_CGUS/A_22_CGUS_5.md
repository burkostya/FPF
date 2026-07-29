---
source: FPF-Spec.md
title: ### A.22.CGUS:5 - Worked Slices
level: 3
part: A
---
### A.22.CGUS:5 - Worked Slices

**Architecture P2S slice.** A team starts with architecture-relevant problem pressure. The unfolding structure may relate problem pressure, unknown structures, candidate structures, architecture characteristics, one `ProjectArchitectureDecision@Context` governed by `C.32.PAD`, realization-work linkage, actual-structure feedback, and return conditions. The P2S flow card can describe those relations, but the decision relation remains governed by `C.32.PAD`, architecture descriptions by `C.30.AD`, and planned or performed work by the A.15 family.

**Abductive search slice.** An inquiry starts from an abductive prompt and a cue set selected for the search. The unfolding structure may relate rival hypotheses, plausibility constraints, hypothesis-generation positions, evidence-return relations, and downstream tests. The structure is not evidence; evidence appears only when an evidence pattern governs the claim.

**Improvement-loop slice.** A pattern version has an evaluation frame and current evaluation result. The unfolding structure may relate E.22 `CandidateImprovementProposalRow@Context` values, protected tradeoffs, scale-qualified E.23 `ExpectedEvaluationResultChange@Context` predictions, one `ImprovementLoopDecisionValue`, and re-evaluation. The loop is not improvement by shape; `E.23` governs repeated improvement only after the object version, evaluation frame, proposal rows, expected result changes, loop decision, and stop or return boundaries are recoverable.

**First-entry seed slice.** A README entry says "develop or review architecture." That line may seed an entry unfolding among problem-side records, candidate first governed records, likely governing-pattern returns, and next readable outputs. The README line is a seed description, not the project's unfolding structure and not a universal FPF route.

**Field-filled scaffold slice.** A team has a visible card sequence "problem pressure -> candidate options -> eval -> repair." At first this is a `ProvisionalUnfoldingDemonstrationDescription@Context` about the cooling-design question and proposed continuations. After every admission coordinate below is recoverable, the team may admit the wider CGUS and create a separate demonstrative slice over it:

```text
acceptedStartingRecordReferenceRefs[]: ProblemCard@Cooling-v2 through one acceptedStartingRecord reference; EvaluationResult@thermal-margin-v1 through one acceptedStartingRecord reference
acceptedStartingStructureRefs[]: CurrentModulePlacementStructure@Cooling-v2
declaredStructureSubstrateRef: ArchitectureCandidateSynthesisAndImprovementStructure@Cooling-v2
structurePositionRefs[]: PressurePosition; CandidateSetPosition; EvaluationResultPosition; RepairProposalPosition; ReturnPosition, each with one SlotSpec and direct governing pattern
relationSignatureRefs[]: CandidateEvaluatedByResult; ProposalChangesCandidate; ResultConstrainsDecision; ReturnTargetsGoverningPattern
constraintReferenceRefs[]: ThermalMarginConstraint; ServiceAccessConstraint; AcceptedLossBoundary, each through an exact constraint reference relation
invariantReferenceRefs[]: MaintainableCoolingPathInvariant through one invariant reference relation
guardedTransitionReferenceRefs[]: RepairAdmissionGuard through one guarded-transition reference relation; the guard admits repair only after the evaluation-result relation is current
preservedStructureRefs[]: CandidateAlternativeStructure; RepairLocalityStructure
structureInformationAdequacyNoteRefs[]: TeachingSliceAdequacyNote@Cooling-v2 under C.33, recording omitted rejected-candidate detail and its declared-use effect
admissibleNextFormKindRefs[]: U.Structure for a C.32 candidate-palette update; U.Episteme for an E.22 candidate-improvement proposal row; U.Relation for an ArchitectureDecisionRelation@Project under C.32.PAD
admissibleUseRef: use for planning and demonstrating relations among current positions
nonAdmissibleUseRef: do not infer performed-work order, authorization, or architecture decision from the slice
structureUseReturnBoundaryRefs[]: return to C.32 when a new candidate structure appears; return to E.23 when the changed object version is evaluated
stopBoundaryRef: stop stronger candidate-set or evaluation use when the candidate-set or evaluation relations are no longer recoverable
```

The same visible chain helps planning because each position asks for a slot. It does not make the project follow that order and does not authorize work.

**Local relation repair slice.** Later `EvaluationResult@thermal-margin-v2` becomes the current result for the same cooling candidate. Keep the candidate set, structure positions, service-access constraint, maintainable-cooling-path invariant, and return boundaries. Replace only the referenced `CandidateEvaluatedByResult` relation instance, then re-evaluate `RepairAdmissionGuard` under its direct governing pattern. If the new result does not satisfy the guard, remove `repair candidate` from the admissible next forms and update the demonstrative slice that showed that branch; the unrelated `accept candidate` continuation remains live. A changed result therefore repairs one relation and its dependent guard before it changes a wider graph.

**Schema-completion proxy failure.** A team counts filled CGUS fields and adds weakly used references until the completion count rises. Update effort then grows, practitioners stop repairing changed relation instances, and wrong next-form choices increase. The count describes field population only; it does not establish recoverability, currentness, or practical value. Remove references without a receiving use, evaluate whether practitioners recover the correct live alternatives and smallest repair, and use `E.13` when field completion is substituting for those outcomes.

**Reference-currentness slice.** A SoTA pack relies on telemetry and admitted publication editions that can decay. CGUS may relate the current reference set, edition-shift relations, decay triggers, possible deprecation or reship records, and a return boundary. The structure is not the currentness claim; `G.11` governs freshness, telemetry, decay, deprecation, reship, and no-change claims.

**Physical-modeling slice.** A team models a physical system or another governed EntityOfConcern whose behavior depends on component relations, conservation-like constraints, operating modes, calibration data, and analysis goals. CGUS may relate the model structure, admitted measured data, mode-change relations, compiler boundary, solver boundary, surrogate-substitution relation, and returns to calibration or model-discovery work. In a digital-twin case, the physical entity, digital model, measured-data history, simulation outputs, services, and bidirectional correspondence relations keep their exact kinds and direct governing patterns. A simulation run, generated code, exchange package, AI-assisted model edit, calibration result, and digital-twin publication are separately governed results. Acausal modeling is useful here because it shows that relations and constraints can be stated before a calculation direction is chosen; `C.29`, `G.11`, `E.23`, evidence patterns, and domain DPF patterns govern stronger mathematical, currentness, evaluation, evidence, or domain-validity claims.

**Formal-expression boundary slice.** A team expresses part of the cooling CGUS as a DCR graph or constraint-solver model to check whether the `repair candidate` branch is reachable under `RepairAdmissionGuard`. The expression preserves selected positions, dependency relations, and the guard. It loses direct governing-pattern exits, C.33 adequacy notes, and any relation not encoded in the chosen formalism. Record that preservation and loss under `C.29`, use the output only for the declared reachability question, and return to CGUS before selecting the next form. Satisfiability or reachability does not establish that the expression is the CGUS, prescribe performed-work order, prove architecture adequacy, or authorize work.

**Method-to-work linkage slice.** A method description is admitted because it may realize a governed structure change or change set. CGUS may organize the method relation, work-plan seed, readiness condition, expected structure effect, evidence or gate linkage, and stop condition. It does not authorize work. The method, plan, work-entry readiness, performed work, evidence, assurance, and gate claims remain with A.3, A.15, A.10, B.3, A.20, and A.21.

