---
source: FPF-Spec.md
title: ### A.22.CGUS:4 - Solution
level: 3
part: A
---
### A.22.CGUS:4 - Solution

Select `ConstraintGovernedUnfoldingStructure@Context <: U.Structure` as a thin A.22 specialization of `U.Structure` for constraint-governed unfolding across typed positions and exact governed relations.

A constraint-governed unfolding structure is a `U.Structure` whose typed positions, relation signatures, referenced relation values, constraints, invariants, guarded transitions, preserved structures, C.33 adequacy notes, and governing-pattern exits jointly constrain admissible next forms. It states how admitted starting records and already-current structures participate through exact relations. It makes no displayed-order claim about real work and fixes no cardinality of starting records, starting structures, or resulting records.

Do not read "unfolding" as a chain by default. The unfolding structure may be branching, merging, cyclic, partially ordered, or graph-shaped, and it may leave several alternative next forms live at once. Before the wider structure passes the admission test, a linear chain, seminar order, prompt path, or happy path remains a `ProvisionalUnfoldingDemonstrationDescription@Context`. After admission, a presentation of one traversal may be a `DemonstrativeUnfoldingSlice@Context` whose EntityOfConcern is that admitted CGUS.

#### A.22.CGUS:4.1 - Constraint-governed unfolding structure

```text
UnfoldingStructureReferenceKindValue = acceptedStartingRecord | relationInstance | constraint | invariant | guardedTransition | currentness
UnfoldingStructureBoundaryKindValue = admissibleUse | nonAdmissibleUse | stop | return

ConstraintGovernedUnfoldingStructure@Context <: U.Structure:
  boundedContextRef: U.BoundedContextRef
  declaredStructureSubstrateRef: U.EntityRef, referencing one U.Structure
  entityOfConcernRef: U.EntityRef
  entityOfConcernKindRef: U.KindRef
  specializedStructureRef?: U.EntityRef, referencing one narrower U.Structure
  acceptedStartingRecordReferenceRefs[]: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=acceptedStartingRecord
  acceptedStartingStructureRefs[]: U.EntityRef, each referencing one U.Structure
  relationSignatureRefs[]: U.EntityRef, each referencing one U.Signature
  structurePositionRefs[]: U.EntityRef, each referencing one ConstraintGovernedUnfoldingPosition@Context
  relationInstanceReferenceRefs[]: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=relationInstance
  constraintReferenceRefs[]: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=constraint
  invariantReferenceRefs[]: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=invariant
  guardedTransitionReferenceRefs[]: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=guardedTransition
  preservedStructureRefs[]: U.EntityRef, each referencing one U.Structure
  structureInformationAdequacyNoteRefs[]?: U.EpistemeRef, each referencing one StructuralInformationAdequacyNote@Context under C.33
  admissibleNextFormKindRefs[]: U.KindRef
  demonstrativeSliceRecipeRefs[]?: U.EntityRef, each referencing one U.MethodDescription
  admissibleUseRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  nonAdmissibleUseRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  stopBoundaryRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  structureUseReturnBoundaryRefs[]: U.EntityRef, each referencing one UnfoldingStructureUseBoundaryCondition@Context
  currentnessRelationReferenceRefs[]?: U.EntityRef, each referencing one UnfoldingStructureReferencedValueRelation@Context with referenceKind=currentness
```

The declared substrate is the structure being unfolded, not a topic label or container. `specializedStructureRef` is present only when one narrower `U.Structure` record is current, such as an E.18.3 transformation-flow specialization. That narrower record may point back through its `unfoldingStructureRef`; the reciprocal references state one generic-to-narrower specialization relation and do not create two unrelated unfolding structures. Accepted starting records and accepted starting structures remain different: a record may describe, publish, or evaluate a structure without becoming that structure. Every referenced entity retains its exact kind and direct governing pattern.

#### A.22.CGUS:4.1.1 - Dependent position, reference, and boundary relations

```text
ConstraintGovernedUnfoldingPosition@Context <: U.Relation:
  unfoldingStructureRef: U.EntityRef, referencing one ConstraintGovernedUnfoldingStructure@Context
  positionSlotSpecRef: U.EntityRef, referencing one A.6.5 SlotSpec
  positionFillingRef?: U.EntityRef
  positionFillingKindRef?: U.KindRef
  directGoverningPatternRef: U.EntityRef, referencing one U.MethodDescription
  RelationRefKind: U.EntityRef
  Dependence: bounded-context local to unfoldingStructureRef
  Identity: <unfoldingStructureRef, positionSlotSpecRef, positionFillingRef if present>

UnfoldingStructureReferencedValueRelation@Context <: U.Relation:
  unfoldingStructureRef: U.EntityRef, referencing one ConstraintGovernedUnfoldingStructure@Context
  referenceKind: UnfoldingStructureReferenceKindValue
  referencedValueKindRef: U.KindRef
  referencedValueRef: U.EntityRef
  directGoverningPatternRef: U.EntityRef, referencing one U.MethodDescription
  relationSignatureRef?: U.EntityRef, referencing one U.Signature
  RelationRefKind: U.EntityRef
  Direction: unfoldingStructureRef -> referencedValueRef
  Dependence: bounded-context local to unfoldingStructureRef and referencedValueRef editions
  Identity: <unfoldingStructureRef, referenceKind, referencedValueKindRef, referencedValueRef>

UnfoldingStructureUseBoundaryCondition@Context <: U.Relation:
  unfoldingStructureRef: U.EntityRef, referencing one ConstraintGovernedUnfoldingStructure@Context
  boundaryConditionKind: UnfoldingStructureBoundaryKindValue
  conditionDescriptionRef: U.EpistemeRef
  affectedStructureRef: U.EntityRef, referencing one U.Structure
  boundaryGoverningPatternRef: U.EntityRef, referencing one U.MethodDescription
  conditionalReceivingPatternRef?: U.EntityRef, referencing one U.MethodDescription
  RelationRefKind: U.EntityRef
  Dependence: bounded-context local to unfoldingStructureRef and affectedStructureRef editions
  Identity: <unfoldingStructureRef, boundaryConditionKind, conditionDescriptionRef, affectedStructureRef, conditionalReceivingPatternRef if present>
```

The two `...KindValue` declarations are local closed enumerations, not U-kinds. Position filling ref and kind are both present or both absent. A relation signature is present when the referenced value is a relation. Every boundary names its governing pattern; only `return` names a conditional receiver.

`StructuralInformationAdequacyNote@Context` under C.33 carries captured, expected-but-uncaptured, lost, and hidden structure for a declared use. CGUS does not mint parallel loss or hiddenness fields. A use boundary is not permission, gate passage, evidence, assurance, or currentness refresh by itself.

#### A.22.CGUS:4.2 - Admission test

A readable chain is not sufficient for admission. Use CGUS only when the current structure recovers all of the following:

| Coordinate | Recovery for CGUS admission | Reduced use when absent |
| --- | --- | --- |
| Structure identity | One exact `U.Structure` substrate, bounded context, EntityOfConcern, and kind. | Keep a note, card, description, or method description. |
| Typed positions | More than one SlotSpec-grounded position and any current filling ref-kind pairs. | Keep a list or seed description. |
| Connecting relations | Relation signatures and exact referenced relation instances. | Keep an index until connections are recoverable. |
| Cross-position constraints | Constraints, invariants, guards, branches, joins, cycles, partial orders, or many-to-many dependencies that matter to the use. | Keep a linear presentation as a provisional demonstration description until the wider structure is admitted. |
| Preserved and omitted structure | Preserved structures and any C.33 adequacy notes needed by the declared use. | Lower the adequacy claim and retain the return. |
| Admissible next forms | Exact next-form kinds, not one forced next record. | Do not claim a usable unfolding structure. |
| Direct governing-pattern exits | Each stronger claim points to its direct pattern. | The structure is overreading itself as method, work, evidence, gate, architecture, publication, or refresh authority. |
| Use boundaries | Admissible, non-admissible, stop, and return conditions are explicit. | Keep the artifact as a provisional explanation. |

Branches or joins that are current remain visible. A cycle shown as "return to the start" is not thereby a chain. One slice may be linear because attention needs one path; the wider structure remains graph-shaped when its relations are graph-shaped.

#### A.22.CGUS:4.3 - Provisional demonstrations, admitted-structure descriptions, and demonstrative slices

A presentation may help discover positions and relations before any CGUS exists. Keep that pre-admission object as a C.2.1-conformant episteme about the actual subject-domain object, question, or proposed continuation set:

```text
DemonstrationUseModeValue = workedSlice | firstUseExample | actualCaseReplay | variantComparison | otherDeclared
DemonstrationPresentationFormValue = orderedList | chainDiagram | flowCard | table | narrativePath | slideSequence | promptBlock | graphSlice | otherDeclared

ProvisionalUnfoldingDemonstrationDescription@Context <: U.Episteme:
  entityOfConcernRef: U.EntityRef, referencing the actual subject-domain object, question, or proposed continuation set
  entityOfConcernKindRef: U.KindRef
  boundedContextRef: U.BoundedContextRef
  viewpointRef: U.ViewpointRef
  subjectRef: U.SubjectRef, decoding to <entityOfConcernRef, boundedContextRef, viewpointRef>
  groundingHolonRef?: U.HolonRef
  claimGraph: U.ClaimGraph by value
  referenceScheme: U.ReferenceScheme by value
  editionId
  demonstrationUseMode: DemonstrationUseModeValue
  presentationForm: DemonstrationPresentationFormValue
  provisionalContinuationDescriptionRefs[1..*]: U.EpistemeRef
  candidatePositionDescriptionRefs[2..*]: U.EpistemeRef
  candidateRelationDescriptionRefs[]?: U.EpistemeRef
  unresolvedCGUSAdmissionCoordinateDescriptionRefs[1..*]: U.EpistemeRef
  admissionTransitionConditionDescriptionRef: U.EpistemeRef
```

This local declaration form is an episteme, not a structure slice and not a new root kind. Its C.2.1 identity comes from its exact EntityOfConcern, DescriptionContext, optional grounding holon, ClaimGraph, reference scheme, and edition. `entityOfConcernRef` names the subject that the explanation is currently about; it may not point to a not-yet-admitted CGUS. Candidate positions and relations are claims to investigate, not admitted `ConstraintGovernedUnfoldingPosition@Context` or relation instances. At least one unresolved admission coordinate remains present while the description is provisional.

Once every coordinate in `4.2` is recoverable and the wider `ConstraintGovernedUnfoldingStructure@Context` is admitted, describe that structure without selecting a traversal through it by creating this C.2.1-conformant episteme:

```text
ConstraintGovernedUnfoldingStructureDescription@Context <: U.Episteme:
  entityOfConcernRef: U.EntityRef, referencing one admitted ConstraintGovernedUnfoldingStructure@Context
  entityOfConcernKindRef: U.KindRef, referencing ConstraintGovernedUnfoldingStructure@Context
  boundedContextRef: U.BoundedContextRef
  viewpointRef: U.ViewpointRef
  subjectRef: U.SubjectRef, decoding to <entityOfConcernRef, boundedContextRef, viewpointRef>
  groundingHolonRef?: U.HolonRef
  claimGraph: U.ClaimGraph by value
  referenceScheme: U.ReferenceScheme by value
  editionId
  preservedStructureRefs[]: U.StructureRef
  structureInformationAdequacyNoteRefs[]?: U.EpistemeRef, each referencing one StructuralInformationAdequacyNote@Context under C.33
  declaredUseRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  descriptionUseReturnBoundaryRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
```

Its EntityOfConcern is the admitted CGUS. Its ClaimGraph may describe branches, joins, cycles, partial orders, positions, relations, constraints, and admissible next forms without choosing one route through them. Carrier, diagram form, table layout, or publication location does not determine its identity. A new edition is required when the described CGUS edition, DescriptionContext, applicable grounding, ClaimGraph, reference scheme, preserved-structure account, adequacy account, declared use, or return boundary changes.

When one presentation selects a traversal or ordering through that admitted structure, create a different post-admission episteme:

```text
DemonstrativeUnfoldingSlice@Context <: U.Episteme:
  entityOfConcernRef: U.EntityRef, referencing one admitted ConstraintGovernedUnfoldingStructure@Context
  boundedContextRef: U.BoundedContextRef
  claimGraph: U.ClaimGraph by value
  referenceScheme: U.ReferenceScheme by value
  editionId
  derivedFromProvisionalDemonstrationRef?: U.EpistemeRef, referencing one ProvisionalUnfoldingDemonstrationDescription@Context
  demonstrationUseMode: DemonstrationUseModeValue
  transformationFlowStructureRef?: U.EntityRef, referencing one E.18 TransformationFlowStructure
  pathSliceId?: E.18 PathSliceId
  designRunTag?: E.18 DesignRunTag
  demonstratedPatternUseRowRefs[]: U.EpistemeRef, each referencing one DemonstratedPatternUseRow@Context
  includedStructurePositionRefs[]: U.EntityRef, each referencing one ConstraintGovernedUnfoldingPosition@Context
  omittedStructureInformationAdequacyNoteRefs[]?: U.EpistemeRef, each referencing one StructuralInformationAdequacyNote@Context under C.33
  loopCompressionRuleRef?: U.EntityRef, referencing one U.MethodDescription
  alternativeSliceRefs[]?: U.EpistemeRef, each referencing one DemonstrativeUnfoldingSlice@Context
  presentationOrderingRuleRef: U.EntityRef, referencing one U.MethodDescription
  presentationForm: DemonstrationPresentationFormValue
  admissibleUseRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  nonAdmissibleUseRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
  sliceReturnBoundaryRef: U.EntityRef, referencing one UnfoldingStructureUseBoundaryCondition@Context
```

The transition does not retype the provisional episteme or any subject-domain result. The admitted slice cites the provisional description only as its derivation basis, names the already-admitted CGUS as EntityOfConcern, and replaces candidate position and relation descriptions with exact admitted structure positions and relation references. Its edition changes when that CGUS edition, included positions, omitted-structure account, traversal or ordering rule, alternatives, use boundary, ClaimGraph, or reference scheme changes; carrier or rendering change alone does not. If admission later fails, the provisional explanation may remain useful under its declared use while the slice claim is withdrawn.

The local mode and presentation-form values are enumerations, not CharacteristicSpaces or U-kinds. Presentation form says how the episteme is rendered; it is not a carrier kind. Add an E.17 publication relation only when publication is current.

The E.18 triple is all present or all absent. When present, it locates this post-admission demonstration in one flow valuation and relates pattern-selection, selected-pattern-application, and downstream-subject-work slices without merging their structures, rows, work occurrences, or results.

#### A.22.CGUS:4.3.1 - Demonstrated pattern-use rows

When a local pattern mantra is admitted as a `DemonstrativeUnfoldingSlice@Context`, `mantra move` is bounded Plain wording for one `DemonstratedPatternUseRow@Context` inside that slice. The row consumes A.6.5 SlotSpec discipline, but A.6.5 does not govern the row's identity. The row is not a root U-kind, an operation, or a work occurrence. It shows one result-bearing conditional continuation. A short repeatable formula that only recalls one pattern's Solution may still be a useful local mantra without containing such rows and without becoming a CGUS.

```text
DemonstrationBasisModeValue = publicTemplate | projectCandidate

DemonstratedPatternUseRow@Context <: U.Episteme:
  entityOfConcernRef: U.EntityRef, referencing the containing DemonstrativeUnfoldingSlice@Context
  boundedContextRef: U.BoundedContextRef
  claimGraph: U.ClaimGraph by value
  referenceScheme: U.ReferenceScheme by value
  editionId
  sourcePracticeContinuationDescriptionRef?: U.EpistemeRef, referencing one PatternUsePracticeContinuationDescription@Context
  demonstrationBasisMode: DemonstrationBasisModeValue
  demonstratedResultFlowPosition: PatternUseResultFlowPositionValue
  nestedPatternSelectionSliceRef?: U.EpistemeRef, referencing one DemonstrativeUnfoldingSlice@Context
  actionOrProposedUseDescriptionRef: U.EpistemeRef
  directPatternIdentifier: PatternIdentifierValue
  directPatternName: PatternNameValue
  publicCandidateUseTemplateRef?: U.EpistemeRef, referencing one PublicCandidatePatternUseTemplate@FPFReadme
  projectCandidatePatternUseRef?: U.EpistemeRef, referencing one CandidatePatternUse@Context
  publicPracticalUseQuestionRef?: U.EpistemeRef, referencing one PublicPracticalUseQuestion@FPFReadme
  projectPracticalUseQuestionRef?: U.EpistemeRef, referencing one PracticalUseQuestion@Context
  solutionMethodDescriptionRef: U.EntityRef, referencing one U.MethodDescription
  publicResultTemplateRef?: U.EpistemeRef, referencing one PublicPatternUseResultTemplate@FPFReadme
  projectResultExpectationRef?: U.EpistemeRef, referencing one PatternUseResultExpectation@Context
  publicContinuationConditionRef?: U.EpistemeRef, referencing one PublicPatternUseBoundaryConditionTemplate@FPFReadme
  projectContinuationConditionRef?: U.EpistemeRef, referencing one PatternUseBoundaryCondition@Context
  alternativeDemonstratedRowRefs[]?: U.EpistemeRef, each referencing one DemonstratedPatternUseRow@Context
  returnDemonstratedRowRefs[]?: U.EpistemeRef, each referencing one DemonstratedPatternUseRow@Context
  applicabilityFindingRef?: U.EpistemeRef, referencing one PatternUseApplicabilityFinding@Context
  recommendationRef?: U.EpistemeRef, referencing one PatternUseRecommendation@Context
  workPlanRef?: U.EntityRef, referencing one U.WorkPlan
  performedWorkRef?: U.EntityRef, referencing one U.Work
```

In `publicTemplate` mode, exactly the public candidate, question, result, and continuation positions are filled; the project positions are absent. In `projectCandidate` mode, exactly the project candidate, question, expectation, and continuation positions are filled; the public positions are absent. Applicability, recommendation, WorkPlan, and Work refs appear only when those values already exist.

The result-flow position is always present. An unresolved direct-pattern choice opens a separate nested pattern-selection slice. That slice returns a candidate, finding, or recommendation used by the enclosing row; it does not become the enclosing result-producing structure.

#### A.22.CGUS:4.3.2 - Pre-execution slot-filling scaffold

A provisional demonstration can hold attention on visible candidate positions before execution and before CGUS admission. Each visible position initially points to a subject-domain object, question, or proposed continuation and states which A.22.CGUS admission coordinate remains unresolved. It does not yet point to an admitted `ConstraintGovernedUnfoldingPosition@Context`.

Fill the scaffold in small passes. First name the visible candidate positions. Then recover the exact objects, kinds, relation signatures, constraints, invariants, guards, preserved structures, C.33 notes, next-form kinds, and stop or return conditions that would satisfy `4.2`. Keep every unresolved coordinate explicit in the provisional description. Only after the wider structure is admitted may a separate demonstrative slice replace candidate descriptions with exact structure-position and relation refs.

**Minimal first use.** Write three visible candidate positions such as `candidate`, `evaluate`, and `repair`; describe the proposed relation that would make repair conditional on an evaluation result; and show both `accept candidate` and `repair candidate` as possible continuations. Keep this as a `ProvisionalUnfoldingDemonstrationDescription@Context` while the exact position kinds, relation instance, guard, preserved structure, or use boundary remains unresolved. It already helps a team hold the branch in attention without asserting the wider CGUS.

After CGUS admission, create a separate `DemonstrativeUnfoldingSlice@Context`, cite the provisional description as derivation basis, and map only the recovered candidate material to exact admitted positions and relations. The scaffold helps design the wider graph; neither provisional nor admitted presentation asserts project work order or authorizes work.

#### A.22.CGUS:4.3.3 - Bounded names and bridge

`Mantra` is broader Plain didactic wording for a short repeatable formulation that keeps a local pattern's Solution in attention. The word alone does not recover one universal FPF kind. `A.6.P`, for example, can publish a local RPR mantra that recalls its repair order without claiming a wider unfolding structure.

Other patterns may keep an established local name such as `mnemonic`, `watchword`, or `heuristic` when that name better tells their readers what the aid does. A.19's common-space comparison mnemonic, A.15.1's CAC mnemonic, and E.8's seven-step heuristic need not be renamed `mantra`. Conversely, an acronym, title mnemonic, or retrieval label is not a local mantra merely because it is memorable. These are Plain didactic choices interpreted from the local Solution and reader use, not rival FPF kinds.

This pattern governs only the narrower case in which a local mantra presents admissible conditional continuations through a named wider constraint-governed unfolding structure. In that case, `mantra` may name the admitted `DemonstrativeUnfoldingSlice@Context`, and `mantra move` may name one `DemonstratedPatternUseRow@Context` inside it. Neither label grants method, plan, order, authority, work, or teaching-medium identity.

##### Ordinary bounded use

In public FPF explanation, call the admitted slice a `demonstrative walkthrough`. In the bounded seminar context recorded below, `mantra` is the shorter repeatable name for that same demonstrative episteme. One `mantra move` is a `DemonstratedPatternUseRow@Context`: it names the direct pattern, its Solution, the expected result, and the condition for continuing. Outside this admitted CGUS-demonstrative use, interpret a local mantra from the pattern's own Solution and context rather than forcing it into `DemonstrativeUnfoldingSlice@Context`.

##### Naming settlement and bounded reuse

The F.18 cards below record the selected names for the governed A.22.CGUS values. The separate `LocalSenseBasisRelation@Context` values support the exact local-sense claims. The F.9 Bridge states only the semantic relation between the two exact F.17 cells. A separate ordinary C.2.1 assertion says whether that Bridge is suitable for the named seminar-to-public naming use, and A.10 separately governs reliance on that assertion. The cards carry none of the use direction, correspondence rule, loss tolerance, polarity, reliance, permission, or publication occurrence. `PublicRowStatus=current` and each `UnifiedTermRowRef` cite a separate current F.17 row; neither the card nor its inputs create that row. None adds a step to CGUS application.

```text
NameCardId: NameCard.DemonstrativeUnfoldingSlice.FPFPublic
GovernedValueRef: DemonstrativeUnfoldingSlice@Context
GoverningPatternRef: A.22.CGUS
ReferenceScheme: FPFCoreReferenceScheme
ClaimContent: NameCard.DemonstrativeUnfoldingSlice.FPFPublic.ClaimGraph — complete C.2.1 U.ClaimGraph constituted by all identity-bearing naming-settlement claims designated below
LocalSenseCellRef: SenseCell.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11
LocalSenseBasisRelationRef: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11
TechLabel: DemonstrativeUnfoldingSlice@Context
PlainLabel: demonstrative walkthrough
CandidateSet: [demonstrative walkthrough, mantra, mnemonic walkthrough, solution-story refrain, repeated explanatory walkthrough, pattern-use refrain]
RejectedCandidates:
  mantra -> broader local didactic wording that does not by itself identify this CGUS-demonstrative value
  mnemonic walkthrough -> foregrounds a memory technique rather than the represented structure
  solution-story refrain -> overstates narrative form and refrain structure
  repeated explanatory walkthrough -> is too long to serve as the public label
  pattern-use refrain -> narrows the value although a CGUS slice may demonstrate wider structure
SelectionRationale: the phrase identifies a presented explanatory episteme for a cold reader while the Tech value restores represented structure
BridgeRefs: [Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11]
PublicRowStatus: current
UnifiedTermRowRef: UTS.DemonstrativeUnfoldingSlice.FPFPublic
LineageEntries: demonstrative slice -> cold-reader public Plain label
RefreshCondition: readers treat the phrase as actual traversal, fixed work order, or teaching medium rather than the governed episteme
```

```text
NameCardId: NameCard.DemonstrativeUnfoldingSlice.SeminarTeaching
GovernedValueRef: DemonstrativeUnfoldingSlice@Context
GoverningPatternRef: A.22.CGUS
ReferenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
ClaimContent: NameCard.DemonstrativeUnfoldingSlice.SeminarTeaching.ClaimGraph — complete C.2.1 U.ClaimGraph constituted by all identity-bearing naming-settlement claims designated below
LocalSenseCellRef: SenseCell.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11
LocalSenseBasisRelationRef: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11
TechLabel: DemonstrativeUnfoldingSlice@Context
PlainLabel: mantra
CandidateSet: [mantra, demonstrative walkthrough, mnemonic walkthrough, solution-story refrain, repeated explanatory walkthrough, pattern-use refrain]
RejectedCandidates:
  demonstrative walkthrough -> accurate but too long for repeated seminar speech and does not foreground attention
  mnemonic walkthrough -> foregrounds a memory technique rather than repeatable explanatory content
  solution-story refrain -> overstates narrative form
  repeated explanatory walkthrough -> is too long for the repeated teaching alias
  pattern-use refrain -> narrows demonstrations to pattern use and loses wider CGUS cases
SelectionRationale: repeated-formula and watchword senses support remembered repetition; the Sanskrit analysis instrument of thought supplies the attentional rationale; the seminar-teaching scheme excludes ritual, slogan, method, plan, and work senses
BridgeRefs: [Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11]
PublicRowStatus: current
UnifiedTermRowRef: UTS.DemonstrativeUnfoldingSlice.SeminarTeaching
LineageEntries: seminar teaching concept -> English lexical comparison -> bounded teaching alias over the same governed value
RefreshCondition: readers infer ritual authority, slogan, rote formula, method, WorkPlan, Work, teaching medium, or cannot recover the demonstrated structure
```

```text
NameCardId: NameCard.DemonstratedPatternUseRow.SeminarTeaching
GovernedValueRef: DemonstratedPatternUseRow@Context
GoverningPatternRef: A.22.CGUS
ReferenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
ClaimContent: NameCard.DemonstratedPatternUseRow.SeminarTeaching.ClaimGraph — complete C.2.1 U.ClaimGraph constituted by all identity-bearing naming-settlement claims designated below
LocalSenseCellRef: SenseCell.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11
LocalSenseBasisRelationRef: LocalSenseBasisRelation.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11
TechLabel: DemonstratedPatternUseRow@Context
PlainLabel: mantra move
CandidateSet: [mantra move, mantra row, demonstrated pattern-use row, walkthrough continuation, mnemonic step, solution-story move]
RejectedCandidates:
  mantra row -> foregrounds a table container rather than the conditional continuation
  demonstrated pattern-use row -> is exact but too technical for repeated seminar speech
  walkthrough continuation -> loses the bounded relation to the seminar mantra alias
  mnemonic step -> suggests a fixed serial step and memory technique
  solution-story move -> overstates narrative form and can be read as movement
SelectionRationale: the phrase keeps the bounded mnemonic relation and names one continuation; row fields restore direct pattern, Solution, result, and condition
BridgeRefs: none; expression and governed-row use are interpreted under the same seminar-teaching scheme
PublicRowStatus: current
UnifiedTermRowRef: UTS.DemonstratedPatternUseRow.SeminarTeaching
LineageEntries: bounded mantra alias plus local move wording -> typed demonstrated-pattern-use row
RefreshCondition: readers infer universal Move, physical movement, operation, fixed serial step, PlanItem, Work, or a row detached from its slice
```

The two expressions for the demonstrative slice and the local expression for its demonstrated row resolve through exact F.17 coordinates:

```text
SenseCell.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11:
  ReferenceScheme: FPFCoreReferenceScheme
  LocalSenseId: DemonstrativeUnfoldingSlice-public
  LocalExpression: demonstrative walkthrough
  LocalSenseClaim: one readable demonstration of admissible continuations through a wider constraint-governed unfolding structure
  senseFamily: DemonstrativeExplanation
  NameCardRef: NameCard.DemonstrativeUnfoldingSlice.FPFPublic
  LocalSenseBasisRelationRefs: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11

SenseCell.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11:
  ReferenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
  LocalSenseId: DemonstrativeUnfoldingSlice-mantra
  LocalExpression: mantra
  LocalSenseClaim: a short repeatable explanatory walkthrough used to hold the whole solution structure in attention
  senseFamily: DemonstrativeExplanation
  NameCardRef: NameCard.DemonstrativeUnfoldingSlice.SeminarTeaching
  LocalSenseBasisRelationRefs: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11

SenseCell.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11:
  ReferenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
  LocalSenseId: DemonstratedPatternUseRow-mantra-move
  LocalExpression: mantra move
  LocalSenseClaim: one shown pattern-use continuation with its Solution, expected result, and current condition inside a mantra
  senseFamily: DemonstratedPatternUseContinuation
  NameCardRef: NameCard.DemonstratedPatternUseRow.SeminarTeaching
  LocalSenseBasisRelationRefs: LocalSenseBasisRelation.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11

LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11:
  localSenseCellRef: SenseCell(FPFCoreReferenceScheme, DemonstrativeUnfoldingSlice-public)
  basisEpistemeRef: A.22.CGUS
  basisPublicationUnitRef: A.22.CGUS:4.3.3-Ordinary-bounded-use

LocalSenseBasisRelationDescription.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11:
  entityOfConcernRef: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11
  entityOfConcernKindRef: LocalSenseBasisRelation@Context
  viewpointRef: FPFPublicReaderViewpoint
  claimGraph:
    supportedSenseClaim: one readable demonstration of admissible continuations through a wider constraint-governed unfolding structure
    admittedUseClaim: support the public local-sense line for this scheme-based coordinate
    nonAdmittedUseClaim: no evidence, authority, work-order, or naming decision follows from this relation
  referenceScheme: FPFCoreReferenceScheme
  editionId: 2026-07-11

LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11:
  localSenseCellRef: SenseCell(FPFSeminarTeachingReferenceScheme-2026-07-11, DemonstrativeUnfoldingSlice-mantra)
  basisEpistemeRef: SeminarExpression.FPFPracticalUse.2026-07-11
  basisPublicationUnitRef: SeminarExpression.FPFPracticalUse.2026-07-11.Slides8-10

LocalSenseBasisRelationDescription.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11:
  entityOfConcernRef: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11
  entityOfConcernKindRef: LocalSenseBasisRelation@Context
  viewpointRef: FPF Seminar Participant Viewpoint
  claimGraph:
    supportedSenseClaim: a short repeatable explanatory walkthrough used to hold the whole solution structure in attention
    admittedUseClaim: support the bounded teaching sense from the seminar expression
    nonAdmittedUseClaim: the slide carrier does not become the sense, naming settlement, method, plan, or work
  referenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
  editionId: 2026-07-11

LocalSenseBasisRelation.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11:
  localSenseCellRef: SenseCell(FPFSeminarTeachingReferenceScheme-2026-07-11, DemonstratedPatternUseRow-mantra-move)
  basisEpistemeRef: SeminarExpression.FPFPracticalUse.2026-07-11
  basisPublicationUnitRef: SeminarExpression.FPFPracticalUse.2026-07-11.Slides61-62

LocalSenseBasisRelationDescription.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11:
  entityOfConcernRef: LocalSenseBasisRelation.DemonstratedPatternUseRow.SeminarTeaching.2026-07-11
  entityOfConcernKindRef: LocalSenseBasisRelation@Context
  viewpointRef: FPF Seminar Participant Viewpoint
  claimGraph:
    supportedSenseClaim: one shown pattern-use continuation with its Solution, expected result, and current condition inside a mantra
    admittedUseClaim: support the bounded teaching sense of mantra move
    nonAdmittedUseClaim: the slide carrier does not become the row, pattern use, plan, or performed work
  referenceScheme: FPFSeminarTeachingReferenceScheme-2026-07-11
  editionId: 2026-07-11
```

`F.17:5.1` governs these scheme-based cells and basis relations, including their SlotKinds, value and reference kinds, direction, dependence, obtaining condition, and identity. The retained `@Context` suffix names lineage-compatible bounded local use; it introduces no context participant or `U.BoundedContext` slot.

`SeminarExpression.FPFPracticalUse.2026-07-11` names the seminar-content episteme. The publication occurrence that makes one edition available and the `.pptx` and extracted Markdown carriers remain separate. The public basis relation instead uses the current A.22.CGUS pattern episteme as its basis and narrows that basis to the ordinary-use publication unit.

The cross-scheme relation and the row's named use are different objects:

```text
BridgeOccurrence:
  BridgeOccurrenceRef: Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11
  SourceSenseCellRef: SenseCell.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11
  ReceivingSenseCellRef: SenseCell.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11
  BridgePredicateProfile:
    BridgeKind: Narrower-than
    RelationOrientation: source SeminarTeaching sense is narrower than receiving FPFPublic sense
    EndpointSenseReadings: both are DemonstrativeExplanation senses of the governed A.22.CGUS value; the seminar sense additionally requires repetition and attentional use
    RelationSpecificCondition: every demonstrative episteme classified by the seminar sense is also classified by the public walkthrough sense, while some public walkthroughs are not seminar mantras
    ApplicabilityOrAsOfBasis: FPFCoreReferenceScheme and FPFSeminarTeachingReferenceScheme-2026-07-11 at the named sense editions
    BooleanTruthCondition: true only while the proper-specialization condition holds for those endpoint editions
    RequiredDependencies: both F.17 SchemeSenseCells resolve, their cited local-sense basis claims hold, and the A.22.CGUS governed-value identity remains unchanged

C.2.1 claim about this named use:
  ClaimRef: Claim.DemonstrativeUnfoldingSlice.SeminarToPublic.Naming.2026-07-11
  EntityOfConcern: Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11
  EffectiveReferenceScheme: FPFCoreReferenceScheme
  ClaimGraph:
    ProposedUse: a seminar use of "mantra" points to the public demonstrative-walkthrough term and its governed value
    Direction: SeminarTeaching sense -> FPFPublic sense
    CorrespondenceRule: preserve reference to the same governed A.22.CGUS value and do not infer that every public walkthrough is a mantra
    PermittedLossTolerance: repetition, remembered replay, and attentional function may be omitted; no method, plan, order, authority, Work, or teaching-medium claim may be carried
    Polarity: affirmative

A.10 evidence reliance for this claim:
  EvidenceProvenanceRelationRef: EvidenceUse.DemonstrativeUnfoldingSlice.SeminarToPublic.Naming.2026-07-11
  TargetClaimRef: Claim.DemonstrativeUnfoldingSlice.SeminarToPublic.Naming.2026-07-11
  BoundedEvidenceUse: use the seminar word "mantra" to point to the public demonstrative-walkthrough term and the same governed A.22.CGUS value
  EvidencePaths:
    PublicSenseBasisRecord: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.FPFPublic.2026-07-11 --basisEpistemeRef--> A.22.CGUS --basisPublicationUnitRef--> A.22.CGUS:4.3.3-Ordinary-bounded-use --carriedBy--> _current-pattern-hosts/A.22.CGUS-Constraint-Governed-Unfolding-Structure.md
    SeminarSenseBasisRecord: LocalSenseBasisRelation.DemonstrativeUnfoldingSlice.SeminarTeaching.2026-07-11 --basisEpistemeRef--> SeminarExpression.FPFPracticalUse.2026-07-11 --basisPublicationUnitRef--> SeminarExpression.FPFPracticalUse.2026-07-11.Slides8-10 --carriedBy--> FPF_first_seminar_reworked_slidement.pptx@sha256:325B50C5D062479434ECCABFF0B8B3E316825CAA5E1646A61D25183B90B9CA89 (Git blob e990847d37ddca59d15a9cc434fad15381a2122d) and fpf_first_seminar_slides.content.md@sha256:B38C6F5FBC85CAF9986D2141095C90DAFFAB6F3FEA607ACE7FA6CE60EB18228D (Git blob 34fd989b646aa4dc9f2879cab40d2e6dde989b1b)
    NameSettlementRecord: NameCard.DemonstrativeUnfoldingSlice.SeminarTeaching --carriedBy--> _current-pattern-hosts/A.22.CGUS-Constraint-Governed-Unfolding-Structure.md
    DictionaryEvidenceRecord-MW: Merriam-Webster "mantra" entry, accessed 2026-07-11 --derivedFrom--> https://www.merriam-webster.com/dictionary/mantra
    DictionaryEvidenceRecord-OALD: Oxford Advanced Learner's Dictionary "mantra" entry, accessed 2026-07-11 --derivedFrom--> https://www.oxfordlearnersdictionaries.com/definition/english/mantra
    ReaderCueEvidenceRecord: Zhu, Reinecke, and Mitra, Language Scent, arXiv:2604.03604 (2026) --derivedFrom--> https://arxiv.org/abs/2604.03604; supports contextual cues, not equivalence or fitness for every reader
  EvidenceProducingOrInterpretingWork: absent from this fixture; no Work occurrence is used as a premise
  CurrentRoleAssignment: absent from this fixture
  MethodTrace: absent from this fixture
  CurrentnessAndWindow: applies to the named 2026-07-11 sense as evidenced by the exact current seminar carrier editions above; both Git blobs must resolve, both carrier paths must retain the cited raw-SHA-256 bytes, and the cited NameCard and A.22.CGUS governed value must remain current
  UnsupportedAttemptedUse: reverse substitution, structural inference, or any method, plan, authority, Work, teaching-medium identity, publication occurrence, or other receiving occurrence
  ReopenOrStop: stop this naming use and reopen its A.10 classification if either cited Git blob does not resolve, either carrier path no longer contains its cited raw-SHA-256 bytes, any other cited item or provenance edge is missing or stale, either sense, NameCard, or governed value changes, or reader evidence shows that "mantra" obscures rather than locates the public value
  RelianceDisposition: pass only for the named bounded naming use while every path and currentness condition above holds
  B.3 branch: no assurance claim is made and this reversible naming use does not meet the material-reliance threshold
BridgeCard:
  EntityOfConcern: Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11
  EffectiveReferenceScheme: FPFCoreReferenceScheme
  ClaimGraph:
    ClaimMode: actual
    BridgeClaim: Bridge.DemonstrativeUnfoldingSlice.SeminarTeaching-To-FPFPublic.2026-07-11 obtains under the BridgePredicateProfile above
    BoundedUseClaimRef: Claim.DemonstrativeUnfoldingSlice.SeminarToPublic.Naming.2026-07-11
    EvidenceProvenanceRelationRef: EvidenceUse.DemonstrativeUnfoldingSlice.SeminarToPublic.Naming.2026-07-11
    RelianceDispositionClaim: pass only for the named SeminarTeaching-to-FPFPublic naming use
    ObservedLossClaim: the broader public sense does not require repeated speech, remembered replay, or the seminar attentional function
    CounterExampleClaim: a public demonstrative walkthrough may be read once and understood without being repeated or used as a mnemonic
    CurrentnessClaim: use this card only while the named Bridge, bounded-use claim, evidence-provenance relation, local reliance disposition, 2026-07-11 sense editions, and current A.22.CGUS governed value remain current
    NearestNonUseClaim: do not use it for FPFPublic-to-SeminarTeaching substitution or to infer a method, plan, order, authority, Work, teaching-medium identity, publication occurrence, or other receiving occurrence
```

The Bridge is `Narrower-than` because the seminar sense adds repetition and attentional use. That relation orientation grants no use. The separate affirmative claim states the exact SeminarTeaching-to-FPFPublic naming use, direction, rule, and tolerance; the A.10 relation and `RelianceDisposition=pass` support reliance only on that claim. The B.3 branch is absent because no assurance claim is made and this bounded reversible naming use stays below its material-reliance threshold; a later threshold would require B.3's first-claim decision and would not create a positive claim. Neither the NameCards, Bridge, claim, card, nor passing disposition authorizes publication, makes an E.17/E.24.PUB publication occurrence obtain, or proves that publication Work occurred.

The Bridge governs only these two senses of the CGUS-demonstrative value, not every local pattern mantra, and it does not establish the independently governed value identity. The seminar-content episteme supplies the teaching problem and local-sense basis; its publication occurrence and carriers do not. Current English dictionary evidence bears on the lexical choice but does not establish the Bridge or the bounded-use claim by itself. F.18 and reader-use evidence decide the names. A changed NameCard reopens naming without silently changing either sense. A changed SenseCell address, basis-episteme edition, or cited publication unit reopens the corresponding `LocalSenseBasisRelation@Context`; a changed supported-sense claim or use boundary opens another `LocalSenseBasisRelationDescription@Context` edition. A changed Bridge endpoint or profile reopens the relation, while a changed proposed use, rule, tolerance, evidence, or reliance reopens only its separately governed claim or reliance object.

#### A.22.CGUS:4.4 - Direct Governing Pattern Exits

CGUS carries the unfolding structure. It does not absorb stronger claims.

| Stronger claim being made | Direct governing pattern or family |
| --- | --- |
| Atomic bounded change | `A.3.4` |
| Method or method description | `A.3.1`, `A.3.2`, and method-composition patterns |
| Work plan, work entry, or performed work | `A.15.2`, `A.15.5`, `A.15.1`, and neighboring work patterns |
| Evidence, assurance, or gate | `A.10`, `B.3`, `A.20`, `A.21`, `G.6` as current |
| Architecture use, architecture decision, or architecture description | `C.30`, `C.30.ASV`, `C.32.P2S`, `C.32.PAD`, `C.32.ADR`, `C.30.AD` |
| Variant archive, non-dominated front, live pool, or selected-set publication | `C.18`, `C.19`, `G.5` |
| Narrative rendering or publication use | `A.6.3.NAR`, `E.17`, `E.17.0` |
| Improvement of an object version | `E.23`, with evaluation patterns for the declared object |
| Source currentness, decay, edition shift, or refresh orchestration | `G.11` |
| Mathematical lens or formal modeling | `C.29`, `A.6.0`, `A.6.1` |

Use the word `refresh` only when a currentness, telemetry, edition, decay, or slice-local refresh claim is actually current. Otherwise use plain return, stop, split, or repair wording and name the direct governing pattern.

#### A.22.CGUS:4.4a - Direct Governing-Pattern Dependent Records

Some CGUS uses need dependent records that keep adjacent method, work, evidence, architecture, description, or publication claims inspectable. A.22.CGUS does not define those record schemas. Reliance on a stronger claim is admitted only when the corresponding CGUS field names its direct governing pattern.

For method and work linkage, use `MethodWorkUnfoldingLinkage@Context`, governed by A.15, only when a named receiving use relies on that relation remaining inspectable across method, method description, role assignment, capability-fit condition, work plan, readiness, performed work, evidence, assurance, or gate positions. If only one method, work-plan, readiness, performed-work, evidence, assurance, or gate claim is current, use that direct governing record instead.

For architecture use, use the C.32.P2S-owned `ArchitectureUnfoldingStructureUse@Project` only when a named unfolding structure is being used as architecture-relevant structure in problem-to-structure architecturing. If the current claim is only grounded architecture, structural view, architecture description, decision, ADR-like projection, measurement, eval, or performed realization work, use the direct pattern for that claim.

In `ArchitectureUnfoldingStructureUse@Project` and `ArchitectureDecisionRelation@Project`, `@Project` is a compatibility and retrieval cue only. It establishes no project entity, composite-work identity, context, authority, or parthood. When the current use is genuinely local to one actual project, C.32.P2S or C.32.PAD must name the exact composite `U.Work` and the direct relation that connects the unfolding-structure use or architecture decision to that work. A.22.CGUS neither infers nor owns that project-work relation.

This keeps A.22.CGUS thin: it governs the constraint-governed unfolding structure and its safe next-use boundary, while A.15, C.30, C.32, evidence, gate, publication, and domain patterns govern the adjacent records that carry stronger claims.

#### A.22.CGUS:4.5 - Promoted Core Family Cue Examples

The FPF core may promote a few short family cues when a cue helps readers recover a familiar governing pattern and a common blocked overread. This is an example device, not a maintained list of all CGUS families.

For example, `UF.P2S` can be useful when an architecture-facing question moves from problem pressure to candidate, selected, expected, or actual structures. The cue points the reader toward `C.32.P2S` and warns that a P2S card is not itself the architecture decision, architecture description, ADR, or realization work.

For example, `UF.IMP` can be useful when an object version, evaluation frame, candidate repairs, and re-evaluation are current. The cue points toward `E.23` and warns that a retry loop or prompt loop is not quality improvement by shape.

For example, `UF.REFRESH` can be useful when a `G.11` source-currentness relation, telemetry, evidence decay, or edition shift is current. The cue points toward `G.11` and warns that a stale reference set is not current authority.

If no promoted cue helps, omit the cue. Do not invent a core `UF.*` cue merely to make a CGUS use look governed. DPFs and project-local frameworks may carry their own local cue examples when useful, but the governing claim still comes from the local governing-pattern map and the relevant pattern bodies.

#### A.22.CGUS:4.6 - Replay and change localization

Replay one CGUS use from its bounded context, unfolded structure, subject EntityOfConcern and kind, current position fillings, exact referenced relation instances, constraints, invariants, guards, preserved structures, C.33 adequacy notes, admissible next-form kinds, and use boundaries. For each selected continuation, recover the relations and guards that admit it and the direct pattern governing any stronger claim. A demonstrative slice is replayable only as one declared presentation of that wider structure.

Localize a change before reopening wider work. A changed relation instance reopens that reference and its dependent guards or continuations. Changed omitted structure reopens the affected C.33 adequacy note and any slice relying on it. A changed presentation changes the demonstrative slice without changing the CGUS unless it reveals missing or false structure. A freshness, edition, telemetry, or decay change is handled by its exact `G.11` relation. A changed method, work, evidence, architecture, publication, or formal claim returns to the direct governing pattern for that claim. Rebuild the wider CGUS only when its structure identity, position set, relation structure, constraints, or declared use boundary has changed.

