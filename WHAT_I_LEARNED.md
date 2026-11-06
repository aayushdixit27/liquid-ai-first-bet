# What I learned from the labs

## Lab 1: On-device

- **Memory is the first limit.** SiMa states 16 GB. Linux sees 5.8 GiB. Check what's usable before promising what fits. (One reading, one board.)
- **Speed wasn't the limit on text.** The accelerator ran the 230M model roughly 5x faster than the CPU. At one check a minute, even the CPU has time to spare. (One run each, with different file formats, runtimes and timing.)
- **Fast isn't the same as useful.** The 230M model said a box at a gate deserved an alert because nobody had reported a problem. That doesn't follow. (One answer.)
- **So I cut the written reason.** The alert is now a flag plus the photo, and a person decides.
- **Which chip a model can use is a product constraint.** LFM3 and d1 have no compiled version for this accelerator, so on this board they run only on the CPU. (I didn't run either in this lab.)
- **Not proven yet:** a real photo, accuracy and energy per check.
- **The bet: kept for now.** It dies if most sites already have power and a good link, or if a photo check takes over 60 seconds.
