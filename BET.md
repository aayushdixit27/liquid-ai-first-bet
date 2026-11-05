# The bet

Written in Lab 1, then updated after each lab. Old versions stay visible.

This is a sample project for a lab. It tests one idea on one board. It is not a product.

## Version 2 (after Lab 1)

**Decision:** Keep the bet for now. I need more information before I change it, specifically what happens when a photo goes through the model. The claim stays as it is in version 1.

**What Lab 1 showed:** The small model fits and runs fast on text. The 4B image model loaded in 14.26 s and gave a short text answer in 1.9 s once loaded. No photo was tested, so "checks a camera photo every minute" is still unproven.

**What would have broken it today:** A model that wouldn't load, or a load and answer time over 60 seconds. Neither happened on text.

**Cut: the written reason in the alert.** The alert is now a flag plus the photo, and the person reviewing it decides.
- Why: I asked the 230M model if a box in front of a gate was worth an alert. It said yes, because nobody reporting a problem suggests the camera may be broken. That reason doesn't follow. A confident wrong reason could mislead the person reviewing the alert, and could send a truck out for nothing.
- What else this gives me: a person sees the photo itself, and each answer in Lab 2 is either right or wrong.
- Limit: this rests on one answer from the small text model. I haven't tested reasons from the 4B model. I'd add reasons back if a real test shows they're reliable.

**Buyer and budget:** Whoever approves the budget for the site, which may be the operations director. I assume it's part of the tech budget. I need to confirm that with a buyer.

**Price:** $25 per site per month, as a placeholder. The missing number is how many incidents a site has each year.
- A truck visit is reported at about $150 to $500 (vendor sources, no agreed benchmark). A copper theft repair is reported at about $4,000 to $6,000 (utilities, mostly 2013 to 2014 reports).
- $25 a month is $300 a year (computed), so one false alarm that sends a truck could use up most of a year's fee.
- Inspections stay in place, so this doesn't save those trips. Catching damage early also doesn't undo it. The value is finding it sooner.

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
- How much energy each photo check uses. A solar site cares about the total energy for each check, not only the wattage on a spec sheet.
