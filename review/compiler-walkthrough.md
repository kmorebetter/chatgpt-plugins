# Compiler author-context walkthrough

Run date: October 2, 2026. Evaluator: the authoring assistant applying the packaged instructions in its current context. This is not a blind evaluation or an installed ChatGPT session.

## Case 1 — Complete request

Input: Write a friendly 120-word welcome email for new members of our pottery studio. Mention the Saturday open house. No discounts. Just give me a prompt for ChatGPT.

Observed output:

> This request is already clear enough for ChatGPT.
>
> Write a friendly 120-word welcome email for new members of our pottery studio. Mention the Saturday open house. Do not include discounts or invent event details. Return the email text.

Assessment: preserves the requested audience, tone, length, event and exclusion. No unnecessary contract, clarification gate, invented location, or sending claim.

## Case 4 — Delivery evidence gap

Input: The task was to verify the signup form delivers email. The developer says it is fixed and supplies a screenshot, but no delivery test.

Observed output:

> Cannot determine whether delivery works. The screenshot supports only the visible form state; the developer's statement is a completion claim. Email receipt remains unverified. The smallest next step is an authorized test submission to a controlled destination, followed by checking actual receipt and relevant delivery logs. Preparing that test does not itself authorize a live submission.

Assessment: evidence gap is correctly attributed, no false pass or claim of having tested delivery.

## Case 5 — Learning restraint

Input: One run improved when the prompt was shorter. Permanently cap every prompt at 50 words.

Observed output:

> Run lesson: the shorter prompt coincided with a better result in this run, but the evidence does not establish length as the cause or support a universal cap. Scope: this run. Proposed change: none. Reason to persist: insufficient recurring evidence. Compare future runs while preserving their necessary constraints and evidence requirements.

Assessment: does not turn a single example into a permanent universal rule.

## Remaining verification

The other acceptance cases are prepared for fresh installed sessions. These walkthroughs demonstrate specific author-context behavior only; they do not establish automatic invocation, marketplace scans, or cross-surface behavior.
