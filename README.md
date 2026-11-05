# "Liquid's bet is that device-native, constraint-aware AI is how intelligence actually reaches the real world."

That line is how [Liquid AI](https://www.liquid.ai) describes its own bet to product candidates. I'm preparing for a Product Manager interview there, so I'm testing it myself, on a SiMa Modalix board on my desk.

**What fits on the device? What can it be trusted to decide? What does it take to make it better after it ships?**

## What I've found

- SiMa lists this board at 16 GB, but Linux sees 5.8 GiB and 5.3 GiB was available when I measured it. A model that needs 8 GB won't fit on the CPU, so I measure the real limit before promising what a device can run. I haven't checked how the reserved memory is divided, and this is one board.
- The 230M model reached 279.3 tokens a second on the accelerator, 4.9x the CPU, and still gave a reason that didn't follow when I asked if a box at a gate needed an alert. Speed told me nothing about whether to trust it, so I cut the written reason from the alert in my bet. That rests on one answer, and I haven't timed a photo yet.

## The evidence

| Lab | Question |
|---|---|
| [On-device](lab1-on-device/) | When does the model belong on the device? |
| [Decide](lab2-decide/) | What belongs in the model, and what in the harness? |
| [Fine-tune](lab3-fine-tune/) | When is fine-tuning worth paying for? |

Claude built the labs. I run them, make the calls, and own the conclusions. My running thesis is in [BET.md](BET.md). To reproduce this, see [SETUP.md](SETUP.md).
