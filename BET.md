# The bet

Written in Lab 1, then updated after each lab. Old versions stay visible.

This is a sample project for a lab. It tests one idea on one board. It is not a product.

## Version 1 (Lab 1, before any measurements)

**Vertical:** Remote utility and pipeline sites.

**Use case:** A camera checks a site once a minute. A model on the device reviews each photo. The satellite link stays off unless the model flags a problem or a photo is picked for random review. Then a cloud model or a person checks it. This adds to inspections and does not replace them.

**Buyer:** Operations director at a utility or pipeline operator.

**Why now:** Models that can read an image now fit on a small board. Satellite broadband is easy to buy, but it needs more power than some sites have.

**Claim:** A small AI model on a box at a remote site can spot problems that last, like a cut fence. It checks a camera photo every minute. It asks the cloud for help on fewer than 1 in 20 photos and misses fewer than 1 in 20 problems. I'm wrong if it can't hit those numbers, or if it uses too much power for a site that can't run a satellite dish all day.

The limits in the claim are targets I chose. None of them has been measured yet.

**Scope limits:**
- One board, in a lab. No field deployment.
- Lasting physical problems only. Brief events, like a person walking through, are out.
- Runs unattended. People only review what gets flagged.
- Not for safety-critical monitoring on its own.

**Still unproven:**
- Whether these sites really lack power or a good link. If most have both, the bet is dead.
- How often these sites get inspected today, which sets the bar to beat.
- Whether a buyer will act on an alert.
