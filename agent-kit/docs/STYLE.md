# Style

<!-- The writing rules for every user-facing text: docs, UI copy, error
     messages, release notes. Based on Simplified Technical English.
     AGENTS.md house style governs code; this file governs words. -->

jev-curate uses one voice for every text.
The rules keep the text short, clear and easy to translate.

## Rules

1. Write one instruction in one sentence.
2. Keep an instruction under 20 words.
3. Keep a descriptive sentence under 25 words.
4. Use the active voice.
5. Use the simple present tense.
6. Use one word for one idea. Do not use synonyms.
7. Do not use contractions.
8. Do not use marketing words.
9. Start an instruction with the verb.
10. Use a list for a sequence of steps.
11. Use a table for a set of values.
12. Write numbers as digits.

## Command line

The CLI prints tables and one-line errors. An error names the fix in the same line
("Live Jev requires TYPESAFE_API_KEY. Export your key or pass --mock for offline tests.").
No tracebacks for expected failures. No progress chatter.

## Terms

<!-- One word for one idea, enforced. Grow this table as terms appear. -->

| Use | Do not use |
|---|---|
| gate | check, rule, filter, test, question |
| rubric | config, spec, recipe |
| row | record, example, line, sample |
| kept / rejected | passed / failed, accepted / dropped (a gate passes or fails; a row is kept or rejected) |
| run | job, batch, session |
| output dir | run dir, workspace |
| live / mock | real / fake, prod / test |
| Jev | the model, the judge, the LLM |
| resume | restart, continue |
