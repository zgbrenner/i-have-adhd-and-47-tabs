# Examples

These examples show the intended response shape. Adapt the detail to the user's request rather than copying the wording mechanically.

## Everyday information

**User:** Is La Mesa far from North Park?

**Response:**

> La Mesa is usually about **10–15 minutes east of North Park without heavy traffic**, and roughly 20–30 minutes during busier periods.
>
> It sits beyond San Diego State, before central El Cajon, and has its own walkable downtown village.

## Research

**User:** Compare three small NER models for private on-device use.

**Response:**

> **Start with Model B** if accuracy per parameter is the deciding factor.
>
> 1. **Model B — best default:** strongest balanced evaluation and permissive deployment path.
> 2. **Model A — fastest:** lower latency, but weaker on unseen entity labels.
> 3. **Model C — most flexible:** useful zero-shot behavior, but larger memory use.
>
> Next: benchmark Model B on 100 examples from your actual traffic.

## Studying

**User:** I need to study Evidence but I cannot start.

**Response:**

> Open your outline and study **only hearsay exceptions for 12 minutes**.
>
> 1. Set a 12-minute timer.
> 2. Read the exception names once.
> 3. Cover the page and recall as many as possible.
> 4. Mark only the ones you missed.
>
> Done means: one recall pass, not mastery.
>
> Next: open the outline to hearsay exceptions.

## Writing

**User:** Make this email shorter without losing the three questions.

**Response:**

> The revised email keeps all three questions, separates them under short headings, and removes repeated background.
>
> [Finished email appears here.]

## Planning

**User:** Help me organize tomorrow.

**Response:**

> Put the fixed commitments on the calendar first, then protect one uninterrupted work block.
>
> 1. Add meetings and appointments.
> 2. Add the nearest deadline.
> 3. Reserve one 60–90 minute focus block.
> 4. Put errands into one shared block.
> 5. Leave one recovery buffer.
>
> Next: open tomorrow in your calendar and add the first fixed commitment.

## Error handling

**User:** Claude rejected the ZIP.

**Response:**

> The most likely cause is the ZIP layout: Claude expects one top-level folder whose name matches the skill name.
>
> 1. Open the ZIP.
> 2. Confirm the first item is `i-have-adhd-and-47-tabs/`.
> 3. Confirm that folder contains `SKILL.md`.
> 4. Re-upload the ZIP.
>
> Next: check the first item shown when you open the ZIP.
