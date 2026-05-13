---
name: software-architecture
description: Software architecture guidance. Use when designing new systems or subsystems, choosing architectural patterns (microservices, event-driven, hexagonal, CQRS), defining component/service boundaries, planning integration strategies, writing Architecture Decision Records (ADRs), evaluating technology stack choices, or reasoning about non-functional requirements like scalability, reliability, and maintainability.
---

# Software Architecture

Structural thinking for systems that need to evolve, scale, and be operated. Architecture decisions are expensive to reverse — apply deliberate reasoning before committing.

## The Core Job of Architecture

Architecture answers three questions for every significant decision:
1. **What are the components and how do they relate?** (structure)
2. **Why this shape and not another?** (reasoning)
3. **What did we knowingly trade away?** (tradeoffs)

If you can't answer all three, the decision isn't fully made yet.

## Defining Component Boundaries

Good boundaries follow natural seams in the domain. Bad boundaries follow layers (presentation, service, data).

**Heuristics for a good boundary:**
- A component can be understood, built, tested, and deployed without knowing the internals of its neighbors.
- A change inside a component doesn't ripple to others.
- Each component has a single, nameable responsibility that a domain expert would recognize.
- Communication across the boundary uses an explicit, versioned contract.

**Warning signs a boundary is wrong:**
- Two components always change together — they're one component, split at the wrong seam.
- One component directly reads another's database or internal data structure.
- You can't explain what a component does without describing what it calls.

## Architectural Patterns — When to Use Each

### Monolith (Modular)
Use when: team is small, domain is not fully understood, latency between components matters, operational simplicity is a priority.
Don't avoid it because it sounds old — a well-structured modular monolith beats a poorly-structured microservices system every time.

### Microservices
Use when: components need to scale independently, different teams own different services, different services have genuinely different deployment cadences or technology needs.
Cost: distributed systems problems (partial failure, network latency, eventual consistency, distributed tracing). Don't pay this cost until you need the benefit.

### Event-Driven / Message-Passing
Use when: producers and consumers need to be decoupled in time and deployment, multiple consumers react to the same event, high throughput async processing is needed.
Cost: harder to trace causality, at-least-once delivery needs idempotency, debugging across queues requires tooling.

### Hexagonal (Ports & Adapters)
Use when: the core domain logic must be testable without infrastructure (DB, HTTP, hardware), and you expect to swap adapters over time (different DB backends, different sensor drivers).
Strong fit for robotics systems: the domain logic is the control/planning core; the adapters are hardware drivers, ROS topics, and data stores.

### CQRS (Command Query Responsibility Segregation)
Use when: read and write patterns are fundamentally different in shape, scale, or authorization — maintaining separate models for each pays for the added complexity.
Don't use for simple CRUD where reads and writes look the same.

## Quality Attributes and Tradeoffs

Every architectural choice is a tradeoff across quality attributes. Name them explicitly.

| Attribute | Tensions with |
|---|---|
| Performance | Maintainability (optimize = specialize), Reliability (redundancy adds latency) |
| Scalability | Consistency (CAP theorem — distribute = eventual) |
| Reliability | Cost, Complexity (redundancy, circuit breakers, retries) |
| Maintainability | Performance (abstractions add overhead), Time-to-ship |
| Security | Usability, Performance (encryption, auth overhead) |
| Operational simplicity | Flexibility (fewer knobs = less to tune) |

When evaluating options: list which attributes each option optimizes and which it degrades. Make the tradeoff explicit to the team.

## Architecture Decision Records (ADRs)

Write an ADR for every decision that would be expensive to reverse or that future teammates will need to understand. Keep them short — the goal is a permanent record of reasoning, not a design doc.

```markdown
# ADR-0042: Use ROS2 actions for navigation goals

## Status
Accepted

## Context
The navigation subsystem needs to accept goals, provide progress feedback during execution,
and support cancellation. Services don't provide feedback; topics don't have a request-reply
pattern with cancellation.

## Decision
Use ROS2 actions (rclpy action server/client) for all navigation goal communication.
Custom goal, result, and feedback message types will be defined in `nav_msgs_custom`.

## Consequences
- Callers get real-time feedback and cancellation support out of the box.
- Adds dependency on `action_msgs` and requires action server lifecycle management.
- Integration testing requires spinning up an action client — slightly more involved than service testing.
```

Store ADRs in `docs/decisions/` or `adr/`. Number them sequentially. Never delete an old ADR — mark it as Superseded and link to the new one.

## Coupling and Cohesion

**High cohesion**: things that change together live together. **Low coupling**: things that live separately don't depend on each other's internals.

The goal is high cohesion within a component, low coupling between components.

Signs of excessive coupling:
- Changing one component requires changing another (structural coupling)
- One component knows about the internal state or representation of another (data coupling)
- Components share a mutable global or singleton (common-data coupling)

Reducing coupling:
- Communicate through defined interfaces, not shared data
- Use events/callbacks instead of direct calls when the producer shouldn't know who consumes
- Invert dependencies: depend on an interface, not a concrete implementation

## Data Flow Design

Decide early: **who owns each piece of state, and who is allowed to change it?**

- State should live as close to the point of use as possible.
- A component that owns state is the single source of truth for it — all reads and writes go through it.
- Shared mutable state between components is a coupling landmine. Prefer immutable messages passed between components.
- For complex pipelines: name each stage and what data flows between them before writing code.

```
Sensor Driver → [raw scan message] → Filter Node → [filtered scan] → Mapper → [occupancy grid]
```

Drawing the data flow before implementing surfaces assumptions about message shapes, rates, and failure modes.

## Designing for Operations

The system will fail. Design so that when it does, operators can understand and recover it.

- **Health checks**: every service/node should report its own health — not just "alive" but "ready to handle requests."
- **Graceful degradation**: identify which capabilities can degrade independently. The system should be useful even when non-critical components are down.
- **Idempotency**: design operations so they can be safely retried. Especially important for hardware commands and message-based systems.
- **Versioning at boundaries**: version your message types and APIs from the start. Unversioned interfaces make incremental deployment impossible.
- **Rollback plan for every deployment**: if the new version has a problem, how do you revert? Can you? This question should be answered before deployment, not after.

## Evaluation Framework for Architectural Options

When comparing options, structure the comparison:

1. **Fit to current requirements** — does it solve the actual problem?
2. **Fit to likely future requirements** — how many known future needs does it accommodate without rework?
3. **Operational cost** — what does it take to run, monitor, and debug in production?
4. **Team fit** — does the team have the skills to build and maintain it? What's the learning curve?
5. **Reversibility** — how hard is it to change this decision in 6 months?

Don't pick the technically superior option if the team can't maintain it. The best architecture is the one that gets built, ships, and keeps running.
