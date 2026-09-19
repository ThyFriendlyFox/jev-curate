Read agent-kit/ROUTING.md, then ralph/GOAL.md.

Find the first line in the GOAL.md checklist that is not proven true.
Make it true: implement, add or fix its gate or test, run
./verify/verify.sh, and commit at that boundary with evidence in the
message. One checklist line per iteration; no side quests.

Obey agent-kit/AGENTS.md when touching code and agent-kit/TONE.md when
writing words. Docs move with behavior in the same commit.

If every line is proven and ./verify/verify.sh is green, do nothing.
If a line cannot be made true from here, write why in ralph/BLOCKED.md
and stop.
