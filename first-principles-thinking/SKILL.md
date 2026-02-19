---
name: first-principles-thinking
description: Reason from fundamental truths instead of convention. Use automatically when solving problems, making decisions, or evaluating approaches.
---

# First Principles Thinking

Reason from fundamental truths, not patterns or conventions. Break problems down to their atomic components and rebuild understanding from there.

## When to Apply

Use first-principles thinking when:
- Evaluating a solution or approach
- Making architectural or product decisions
- Debugging complex problems
- The "obvious" answer feels unsatisfying
- Conventions conflict with the specific context

## Core Method

**1. Identify assumptions**
List everything being taken for granted. What are we assuming must be true?

**2. Question each assumption**
Ask "why?" until you hit bedrock — facts that cannot be reduced further. If an assumption rests on convention ("that's how it's done"), it's not bedrock.

**3. Decompose to fundamentals**
What are the irreducible components? What do we know is definitively true?

**4. Rebuild from atoms**
Construct the solution using only verified fundamentals. Let the answer emerge from what must be true, not what's familiar.

## Anti-Patterns

Never default to these without explicit justification:
- "Best practice" — why is it best for *this* context?
- "Usually we do X" — why is this situation usual?
- "The standard approach" — who set the standard and under what constraints?
- "Industry convention" — conventions optimize for average cases, not your case

If using a convention, state *why* it applies here specifically.

## Output Format

**For complex decisions:** TL;DR first, then structured breakdown:
```
**TL;DR:** [One-line answer]

**Assumptions challenged:**
- [Assumption] → [Why it doesn't hold / does hold]

**Fundamentals:**
- [Irreducible truth 1]
- [Irreducible truth 2]

**Therefore:** [Reasoned conclusion]
```

**For simpler problems:** Internalize the reasoning; just deliver a better answer.

## Examples

### Example 1: "Should we use microservices?"

**Conventional thinking:** "Microservices are best practice for scaling."

**First principles:**

**TL;DR:** Probably not — your constraints don't match microservices' assumptions.

**Assumptions challenged:**
- "We need to scale independently" → Do we? What's our actual load pattern?
- "Teams need autonomy" → We have 4 engineers. Coordination cost is low.
- "It's industry standard" → Standard for companies with different constraints.

**Fundamentals:**
- Network calls are slower and less reliable than function calls
- Distributed systems have exponentially more failure modes
- Complexity cost scales with team size and system boundaries

**Therefore:** A modular monolith gives us the code separation benefits without the operational overhead. Revisit when team >15 or load requires independent scaling.

### Example 2: "How should we price this product?"

**Conventional thinking:** "Look at competitor pricing and position accordingly."

**First principles:**

**TL;DR:** Price on value delivered, not market position.

**Assumptions challenged:**
- "Competitors have optimized pricing" → They may be wrong, or optimizing for different goals
- "Customers compare prices" → Do they? Or do they compare outcomes?
- "Lower price = more customers" → Often false for B2B; signals quality

**Fundamentals:**
- Customers pay to solve problems, not to buy products
- Price anchors perceived value
- Willingness to pay correlates with problem severity, not feature count

**Therefore:** Calculate the cost of the problem we solve. Price as a fraction of that value. Competitor pricing is a data point, not a constraint.

### Example 3: "We need to add caching to fix performance"

**Conventional thinking:** "It's slow, add Redis."

**First principles:**

**TL;DR:** The database query is the bottleneck, but caching masks the real issue.

**Assumptions challenged:**
- "The page is slow" → Which part? Measured where?
- "Caching will fix it" → Caching adds complexity. Is the root cause understood?
- "We need Redis" → For what access pattern? What's the invalidation strategy?

**Fundamentals:**
- Latency has a source; find it before adding layers
- Caching trades consistency for speed — is that tradeoff acceptable?
- The fastest code is code that doesn't run

**Therefore:** Profile first. The query fetches 10K rows to display 10. Fix the query. Caching deferred until there's a cache-shaped problem.

## Influences

- **Aristotle:** First principles as foundational truths from which other truths derive
- **Feynman:** "What I cannot create, I do not understand" — rebuild from components
- **Musk:** "Boil things down to fundamental truths and reason up from there"

## Remember

The goal is not to reject all conventions — many exist for good reasons. The goal is to *understand* why something is true for your specific context before adopting it. Convention is a starting hypothesis, not an answer.
