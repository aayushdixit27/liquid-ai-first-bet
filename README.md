# "Liquid's bet is that device-native, constraint-aware AI is how intelligence actually reaches the real world."

That line is how [Liquid AI](https://www.liquid.ai) describes its own bet to product candidates. I'm preparing for a Product Manager interview there, so I'm testing it myself, on a SiMa Modalix board on my desk.

**What fits on the device? What can it be trusted to decide? What does it take to make it better after it ships?**

## What I've found

- SiMa lists this board at 16 GB, but Linux sees 5.8 GiB and 5.3 GiB was available when I measured it. A model that needs 8 GB won't fit on the CPU, so I measure the real limit before promising what a device can run. I haven't checked how the reserved memory is divided, and this is one board.
- Fine-tuning took a 230M model from 23 to 56 of 60 on my leak test, and 25 of 26 on unseen secrets. Then it caught none of 5 leaks in new styles, so I lead with that number. Many test rows share templates with the training data, and the new-style test has only 10 rows.
- On 60 fictional bank replies, rules scored 49, Liquid's d1 scored 53, and rules then d1 scored 57, missing 1 leak at a 0.5 threshold. So I'd put a cheap check before the model. d1's prompt defined a leak and the chat model's didn't, and 37 rows are written examples, so that isn't a real-world score.
- The same chat model changed 16 of 60 answers between its CPU and accelerator builds, while its score only moved from 23 to 25. I'd test the exact build I ship. The prompt layout also differed slightly, so I can't blame rounding alone.
- In my site-monitoring bet, vision models took under a second a photo, so accuracy was the problem. On 254 clean gate photos, Liquid's 450M model missed 59% of open gates with 1.4% false alarms, and a 4B model missed 28% with 25% false alarms. Their scores were 2 apart, so the totals hid the choice. Neither met my claim. The photos are from a driveway camera, not a valve site.

## The evidence

| Lab | Question |
|---|---|
| [On-device](lab1-on-device/) | When does the model belong on the device? |
| [Decide](lab2-decide/) | What belongs in the model, and what in the harness? |
| [Photos](lab2b-photos/) | Can a small vision model see a lasting problem? |
| [Fine-tune](lab3-fine-tune/) | When is fine-tuning worth paying for? |

Claude built the labs. I ran Labs 1 and 2 and the first photo tests. For Lab 3 and the clean gate test, I directed from my phone and Claude ran the commands. I made the calls and own the conclusions. My running thesis is in [BET.md](BET.md). To reproduce this, see [SETUP.md](SETUP.md).
