# LangGraph and Multi-Agent Systems

LangGraph is a lower-level orchestration framework for building stateful, multi-step applications by modeling them as graphs. Where a simple chain is a straight line of steps and a basic agent is a single reasoning loop, LangGraph allows arbitrary control flow: branches, loops, and coordination between multiple participants. It is the tool to reach for when an application's logic is too complex to express as a linear pipeline.

## Graphs, Nodes, and Edges

In LangGraph an application is described as a graph. The nodes are units of work — typically a function or a model call that does something. The edges connect the nodes and determine what runs next. Crucially, edges can be conditional: after a node runs, the graph can decide which node to go to based on the current situation. This is what enables branching logic and, importantly, cycles — the graph can return to an earlier node, which is exactly how an agent's reason-act loop is represented.

## Shared State

What ties a LangGraph application together is its state. The state is a shared data structure that every node can read from and write to as the graph executes. When a node runs, it receives the current state and returns updates to it, which are then available to the next node. This explicit, shared state is the backbone of the framework: it carries information — the conversation so far, retrieved documents, intermediate results — from one step to the next, and it makes the flow of data transparent and inspectable. Because the state persists across steps, LangGraph applications are naturally stateful, in contrast to a single stateless request.

## Why Cycles Matter

The ability to express cycles is the main reason LangGraph exists. An agent that reasons, calls a tool, examines the result, and reasons again is fundamentally a loop, and loops cannot be expressed in a strictly linear chain. By modeling the agent as a graph with a cycle, LangGraph makes this loop explicit and controllable: you can see exactly where the agent decides to continue or stop, insert checks between iterations, and limit how many times the loop may run.

## Multi-Agent Systems

A multi-agent system is one in which several specialized agents collaborate, each responsible for a different role, rather than relying on a single agent to do everything. The motivation is the same as dividing labor among people: a focused agent with a narrow set of tools and a clear role tends to perform its task better than one general agent juggling everything. LangGraph coordinates these agents, managing how control and information pass between them.

## Common Multi-Agent Patterns

Several patterns recur in multi-agent design:

- **Supervisor**: a coordinating agent receives the request and delegates it to the appropriate specialist agent, collects the result, and decides what to do next. The supervisor acts as a router and manager over the specialists.
- **Network**: agents communicate more freely, handing control to one another as needed without a single central coordinator.
- **Hierarchical**: supervisors themselves are organized into layers, with higher-level supervisors managing lower-level ones, allowing the system to scale to complex tasks.

## Handoffs and Coordination

The mechanism by which one agent passes control and context to another is called a handoff. A handoff transfers the relevant state — what has been done and what is needed next — so the receiving agent can continue seamlessly. Designing clear handoffs and a well-structured shared state is the central challenge of multi-agent systems: the agents are only as effective as the information they exchange. When this coordination is done well, a multi-agent system can tackle problems that a single agent would struggle to handle, which is why understanding these patterns is increasingly valued in senior engineering interviews.
