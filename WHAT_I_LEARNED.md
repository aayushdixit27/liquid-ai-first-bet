# What I learned from the labs

## Lab 1: On-device

- **Memory is the first limit.** SiMa states 16 GB. Linux sees 5.8 GiB. Check what's usable before promising what fits. (One reading, one board.)
- **Speed wasn't the limit on text.** The accelerator ran the 230M model roughly 5x faster than the CPU. At one check a minute, even the CPU has time to spare. (One run each, with different file formats, runtimes and timing.)
- **Fast isn't the same as useful.** The 230M model said a box at a gate deserved an alert because nobody had reported a problem. That doesn't follow. (One answer.)
- **So I cut the written reason.** The alert is now a flag plus the photo, and a person decides.
- **Which chip a model can use is a product constraint.** LFM3 and d1 have no compiled version for this accelerator, so on this board they run only on the CPU. (I didn't run either in this lab.)
- **Not proven yet:** a real photo, accuracy and energy per check. (As of Lab 1. Photos and accuracy are tested below. Energy still isn't.)
- **The bet: kept for now.** It dies if most sites already have power and a good link, or if a photo check takes over 60 seconds. (As of Lab 1. The bet changed later.)

## Lab 2: Decide

- **Rules plus a model beat either alone.** Out of 60: chat model 23, rules 49, d1 53, rules then d1 57. (60 rows, some written by hand. The chat model's prompt didn't define a leak, so that gap is overstated.)
- **The threshold is a product decision.** At 0.3, 0.5 and 0.7 the score stayed at 57, but missed leaks went 0, 1, 3 and blocked replies went 3, 2, 0. The score alone hides that trade. (Too few rows to prove calibration.)
- **Test the exact build you ship.** The same model changed 16 of 60 answers between the CPU and accelerator builds. (Different quantization and runtime.)

## Photo tests

- **The prompt can decide the result.** A broad prompt said PROBLEM on all 49 photos, for both models. The prompt was at fault, not the models, so I narrowed the question.
- **"Is the gate open?" isn't solved yet.** On 254 clean gate photos, LFM2.5-VL-450M got 185 right, missing 67 of 114 open gates with 2 of 140 false alarms. Qwen3-VL-4B got 187 right, with 32 missed and 35 false alarms. (Driveway cameras, not valve sites. Model alone, not the full system.)
- **Close scores hid different failures.** LFM misses more and Qwen raises more false alarms. LFM is also faster: 105 ms against 443 ms.
- **Neither model meets the 1 in 20 limit alone.** They missed 59% and 28% of open gates. The whole-system claim is still untested.

## Lab 3: Fine-tune

- **Fine-tuning worked where cheaper fixes didn't.** Base 23, with d1's definition 25, with examples 32, tuned 56. The 32 was hollow, because it answered SAFE on 59 of 60. (Mac for the prompt rungs, board for tuned. The 60 rows share templates with the training data.)
- **It held up on new secrets, not new styles.** It got 25 of 26 on secrets it never saw in training, but 5 of 10 on new writing styles, and caught none of the 5 leaks. (Ten rows, written by Claude.)
- **Tuned added little over d1 once rules ran first.** Rules then tuned got 58, against 57 for rules then d1. That's one row, and a custom model needs upkeep.
- **I re-ran training and the board eval myself.** Same settings and seed, 56 of 60 again, and 0 of 60 answers changed.
- **Limit:** the tuned model runs on the CPU only. Reaching the accelerator needs SiMa's Model Compiler, which is a gap in the path from fine-tune to deployment.
- **The bet: changed to the gate question.** Its Version 5 claim is untested.
