---
name: compiler-start
description: Explain The Compiler workflow and route a request to clarification, prompt compilation, result validation, or reusable learning when the user asks how to get started.
---

# Start with The Compiler

Explain in two sentences that the workflow preserves the user's goal, prepares instructions for the tool doing the work, and can check the result afterward. It does not run another model or grant tool access.

If the user already supplied a request, use [compile](../compile/SKILL.md) without another intake. If they supplied a finished result to check, use [validate](../validate/SKILL.md). If they want lessons from a completed run, use [compound](../compound/SKILL.md). Otherwise ask one question: what are they trying to accomplish? Offer a short example before the question only if useful. Do not insist on a named model or local folder.
