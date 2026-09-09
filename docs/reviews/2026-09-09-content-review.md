# Content review — 2026-09-09

Editorial review of the course notes (`notes/`) and the syllabus (`docs/syllabus/`).
Findings are ordered by severity. Nothing here has been changed in the content
itself except where explicitly marked **[fixed]** — the rest are decisions for
whoever owns the course material.

Reviewed at commit `0a73365`.

---

## Blocking

### B1. The required textbook edition does not match the readings

**Where:** `docs/syllabus/index.md` — Required Textbook vs. Tentative Course Schedule

The syllabus requires the **2nd edition** of Russell & Norvig, but every chapter
reference in the schedule is numbered for the **4th edition**. A student who buys
the required book will be reading the wrong chapters all term.

The evidence is not circumstantial. Week 10's topic list is, verbatim and in order,
the section headings of 4th-edition Chapter 19 *Learning from Examples*:

| Syllabus topic (Week 10) | AIMA 4th ed. |
|---|---|
| Forms of Learning | 19.1 |
| Learning Decision Trees | 19.3 |
| Model Selection and Optimization | 19.4 |
| Linear Regression and Classification | 19.6 |
| Ensemble Learning | 19.8 |
| Developing Machine Learning Systems | 19.9 |

"Developing Machine Learning Systems" is new in the 4th edition — it does not exist
in the 2nd or 3rd. The same pattern holds elsewhere: Week 6 → Ch 10 *Knowledge
Representation* (10.1 Ontological Engineering, 10.2 Categories and Objects) and
Week 7 → Ch 12 *Quantifying Uncertainty* (12.1, 12.3, 12.5 Bayes' Rule) both match
the 4th edition section-for-section. In the 2nd edition, learning is Chapter 18 and
uncertainty is Chapter 13.

**Fix:** change the required textbook to the 4th edition. Also re-check the
parenthetical "(Be sure you get the second edition, which has a green cover.)" —
both the edition number and the cover description need to go.

### B2. Two different midterm dates

**Where:** `docs/syllabus/index.md` — Course Evaluation vs. schedule

The evaluation table gives the Midterm Exam as **Nov 17**. The schedule marks
**MIDTERM 1** in Week 6 (**Oct 20**) *and* "Midterm" in Week 10 (**Nov 17**).
Either there are two midterms — in which case the 20% weight and the evaluation
table are wrong — or one of the two schedule rows is a leftover.

### B3. Course material from a different course

**Where:** `docs/syllabus/index.md` — Labs, Term Project criteria, Presentation criteria

Three passages describe a business analytics course, not an AI course:

- Labs: "designed to help you grasp and apply the **business analytics** concepts
  discussed in the previous courses"
- Term Project criteria: "Demonstration of effective use of **business analytics
  tools and methodologies**"
- Presentation criteria: "including the clarity and structure of the report,
  **interactive dashboards**, and visualizations"

These read as copy-paste from another syllabus. The project criteria in particular
never mention AI, so a student following them literally would be graded on the
wrong thing.

---

## Correctness

### C1. The worked example turns toward the *more* obstructed side

**Where:** `notes/02-agent-and-environment.qmd`

The example gives sensor readings left = 80 cm, front = 25 cm, right = 100 cm, and
the model outputs steering −0.65, described as "Turn left". But the right side is
the more open direction (100 cm vs 80 cm). The note opens by saying the network
"predicts the safest movement direction", so the one worked example contradicts the
stated purpose of the model.

This may be deliberate — a real trained network does not always produce the obvious
output — but as the only worked example in the notes, it will read to students as
an error. Either swap the sign so the robot turns toward the open side, or add a
sentence acknowledging that the network's output is learned rather than rule-based.

### C2. Normalization is inconsistent between notes 02 and 03

**Where:** `notes/02-agent-and-environment.qmd`, `notes/03-formal-model.qmd`

Note 02 maps 80/25/100 cm to `[0.8, 0.25, 1.0]`, i.e. divide by 100 cm, which caps
a normalized input at 1.0. Note 03's next state is `[0.60, 0.35, 1.10]` — a value
of **1.10**, or 110 cm, above that ceiling.

Either the divisor is not the sensor's maximum range (in which case say what it is),
or inputs can exceed 1.0 (in which case note 02 should not imply a [0, 1] scale).
Worth resolving explicitly: normalization range is exactly the kind of detail that
breaks a quantized model on real hardware, so it is a teachable point rather than a
nitpick.

### C3. Sign conventions are never stated

**Where:** `notes/02-agent-and-environment.qmd`

"Steering = −0.65: Turn left" is the only place the reader learns that negative
means left. Similarly, speed 0.20 is called "Move slowly" without saying what 1.0
would mean. A one-line statement of the output ranges and conventions would make
the example self-contained.

### C4. Chapter 10 is assigned to two unrelated topics

**Where:** `docs/syllabus/index.md` — Week 6 and Week 11

Week 6 assigns Chapter 10 for Knowledge Representation (correct for the 4th
edition). Week 11 assigns "chap 10" for Natural Language Processing, which is
Chapter 23. Almost certainly a typo.

### C5. Reading "4.33" does not exist

**Where:** `docs/syllabus/index.md` — Week 4

Chapter 4 has sections 4.1–4.5. Given the listed topic ("Search with
Nondeterministic Actions"), this should be **4.3**.

---

## Consistency

### S1. Unit numbering runs I, II, III, II, IV

**Where:** `docs/syllabus/index.md` — schedule

"UNIT II" is used twice: for *Problem Solving by Searching* and again for
*Uncertain Knowledge*. The latter is presumably meant to be its own unit, which
would also renumber Machine Learning.

### S2. Week 5 appears twice

**Where:** `docs/syllabus/index.md` — schedule

Week 5 / Oct 13 is listed under both UNIT II (Constraint Satisfaction, Adversarial
Search) and UNIT III (Knowledge-Based Agents, Logic). One session cannot cover
four chapters; one of these is likely meant to be Week 6, which would cascade
through the remaining rows.

### S3. Quizzes 1 and 2 are missing from the schedule

**Where:** `docs/syllabus/index.md`

The evaluation table schedules three quizzes (Sep 29, Oct 13, Oct 27). Only
"Quiz #3" appears in the schedule's Quizzes & Exams column. The Sep 29 and Oct 13
rows are blank.

### S4. Labs are mandatory but carry no weight

**Where:** `docs/syllabus/index.md` — Important Notes vs. Course Evaluation

"Doing labs and tutorials is mandatory", but the Labs row in the evaluation table
has an empty Grading cell and "TBA" as its due date. The other four components sum
to exactly 100% (30 + 20 + 40 + 10), so there is no weight left to assign. Either
labs are ungraded — and "mandatory" needs qualifying — or the other weights have to
come down.

### S5. Presentation has no due date

**Where:** `docs/syllabus/index.md` — Course Evaluation

The Due Date cell is blank. The schedule puts Presentations in Week 12 (Dec 1),
which is also the Term Project due date.

### S6. The pass rule mixes units

**Where:** `docs/syllabus/index.md` — Course Evaluation

"a total grade of at least 60, with no individual component scoring below 50%" —
the first threshold has no unit, the second does. Presumably both are percentages.

---

## Writing and structure

### W1. Note 02 opens mid-thought

**Where:** `notes/02-agent-and-environment.qmd`, line 5

The page begins "For example, The robot moves forward → …". This was a sentence
continuing from note 01 when the notes were one document; as a standalone page it
opens with a dangling "For example" and no antecedent. (The stray capital in
"For example, The robot" is from the original.)

### W2. Note 01 opens with an unbound pronoun

**Where:** `notes/01-ai-model.qmd`, line 7

"It is a realistic example of an AI agent running directly on a microcontroller."
There is no antecedent for "It" — the page title is the only referent.

### W3. The interaction loop is an image with no text

**Where:** `notes/02-agent-and-environment.qmd`

The section "The complete interaction loop" consists entirely of a figure whose alt
text is "Interaction loop". A reader using a screen reader, or anyone whose images
fail to load, gets nothing. The loop is the central concept of the three notes and
deserves a prose description or a text diagram alongside the image.

The file is also a 1 MB PNG; re-encoding or resizing would noticeably speed up the
page.

### W4. Overlapping section structure

**Where:** `notes/01-ai-model.qmd` ("The agent and environment") and
`notes/02-agent-and-environment.qmd` ("Agent")

Both notes have a section introducing the agent. The split between the two pages is
a legacy of the original file boundaries rather than a topic boundary.

### W5. Spurious parentheses in the formal notation

**Where:** `notes/03-formal-model.qmd`, lines 12–14

The definitions are written `$(s_t)$`, `$(a_t)$`, `$(s_{t+1})$`. The parentheses are
not part of the notation and do not appear in the equations above them.

### W6. Landing page described sections that no longer exist **[fixed]**

**Where:** `index.qmd`

The syllabus link read "schedule, evaluation, and course policies" after the policy
sections had been removed from the syllabus. Corrected in this commit.

---

## Gaps

Not defects, but the notes stop short of what the syllabus promises. The learning
objectives include implementing an algorithm "to meet correctness and efficiency
requirements", and the notes cover the architecture and the agent loop without
touching:

- **Training.** How the network is trained, what the labelled data is, and where
  ground-truth "safest direction" comes from. This is the hardest part of the
  example and it is currently one clause ("would be trained on a computer").
- **What INT8 quantization actually does.** All values shown are floating point.
  The relationship between the float values in the notes and the int8 values on the
  device — scale, zero point, and the accuracy cost — is the reason the example is
  about a microcontroller at all.
- **Model size.** The `3 → 16 → 8 → 2` network has 218 parameters. Stating that
  makes the "fits on an MCU" point concrete.
- **Timing.** An RTOS task chain implies a deadline. Inference latency and control
  loop rate would connect the AI content to the embedded content.

## Note on naming

`STM32Cube.AI` is ST's older name for the tool; it is now shipped as **X-CUBE-AI**.
The old name is still widely used and understood, so this only matters if students
will be searching ST's site for it.
