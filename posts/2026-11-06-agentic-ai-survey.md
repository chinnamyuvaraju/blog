---
title: What should we measure in an AI agent?
summary: Three questions to ask about tools, coordination, and recovery, drawn from a co-authored survey in Frontiers in Neuroinformatics.
tags: [AI Agents, Research]
---
An AI agent may call a tool, inspect the result, and decide what to do next. That sequence gives us more to evaluate than the final answer alone.

When reviewing an agent experiment, ask:

1. **Tools.** Did the agent pick the right tool and use its output correctly?
2. **Coordination.** If more than one agent was involved, which decisions depended on a handoff?
3. **Recovery.** What did the system do when a tool failed or returned incomplete data?

Try logging the steps for a single task. Run it again with one tool unavailable and compare the traces. You may learn more from the recovery attempt than from a successful run.

## Publication

Saikiran Gogineni, Mohd Dilshad Ansari, Yuvaraju Chinnam, and G Suryanarayana. [Agentic Artificial Intelligence: A Survey of Architectures, Multi-Agent Collaboration, Evaluation and Open Challenges](https://doi.org/10.3389/fninf.2026.1998090). *Frontiers in Neuroinformatics*.

## LinkedIn caption draft

> When you evaluate an AI agent, look at what it did along the way. Which tools did it choose? How did it handle a handoff? What happened when a tool failed? Our survey in Frontiers in Neuroinformatics looks at how agent systems are built and evaluated. I'd be interested to hear which failures you find hardest to measure.
