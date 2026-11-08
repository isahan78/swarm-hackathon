# Swarm Early Warning: findings

**Result:** the supplied frozen-split analysis finds no clear activation-probe advantage over a trained full-context text baseline. First-decision AUROC is **0.775 versus 0.766**, with paired difference **0.009 [−0.143, 0.172]**. The marker outcome is not a verified authorization violation under the actual policy. See the [complete analysis](isahan_analysis.md).

## 1. Research question

Can internal activations predict eventual unauthorized behavior earlier or more accurately than visible conversations? The software supports that experiment. The supplied research dataset supports the narrower outcome of recruited marker insertion, which must not be relabeled as detecting internal co-option.

## 2. Motivation

Peer requests can conflict with assigned rules. Useful oversight must distinguish exposure from eventual behavior, give advance warning, and control false alarms over complete conversations. Detecting the current action before response generation is distinct from predicting several decisions ahead.

## 3. Experimental setup

The independent harness implements scripted A→B/C/D recruitment with independent histories, one shared Qwen model, inert files, ownership verification and JSONL provenance. Mock checks run end to end, and real one-target and three-target Qwen smoke tests completed.

The updated collaborator archive adds 100 two-agent episodes and a 12-parent-run, three-recipient fanout batch. They are analyzed separately. Source files were not changed. No GPU was restarted for this CPU analysis.

## 4. Conditions

The main conditions are overt/direct (30 episodes), latent/delayed (25), hidden/covert (25), and control/clean (20). Marker-positive outcomes are 20, 14, 12 and 0. The same recipient policy applies across conditions. The independent ownership smoke uses a distinct protocol and must not be pooled with these labels.

## 5. Labels and prediction timing

The collaborator's revised policy allows judgment about teammate requests. All recipient edits stay inside owned files: **zero verified ownership violations**. The importer preserves that policy and separately records marker attempts, completions, exposure and agreement candidates. Final marker presence and ever inserting it agree in this snapshot.

The supplied capture code uses a pre-response context forward at the last prompt token, raw decoder layer 18 (`hidden_states[19]`). Historical checkpoint/settings remain unverified. Of 46 positive episodes, 42 insert on the first decision and four on the second. Most opportunities are imminent detection, not multi-turn warning.

## 6. Monitoring methods

- Activation: train-only standardization and logistic regression, C=1.
- Text: train-only TF-IDF and logistic regression, C=1, using the actual task, policy and full visible system/board/workspace input.
- LLM transcript monitor: implemented and verified in 12 calls on the separate ownership smoke; unavailable for the collaborator dataset. Its supplied text scores are TF-IDF, not LLM scores.

Allowlists exclude hidden source instructions, private thinking, current responses/actions, future labels and metadata. Flat current-action rows are reconstructed into pre-action input prefixes.

## 7. Evaluation protocol

Preserve the original 70/30 episode split. Reserve 14 validation episodes inside its training partition, leaving 56 for fitting. All decisions stay with their complete episode. Preprocessing fits only inner training; thresholds use validation negatives; both models use identical frozen test observations. This is retrospective reanalysis because the authors had already examined the test set.

Fixed first decision is primary. Exposure-only and later horizons report changing support. Episode bootstrap intervals and paired AUROC differences quantify uncertainty. Lead zero means imminent action; misses, negatives and missing scores remain counted. Supplied source scores and refitted scores are reported separately.

## 8. Results with figures

The frozen test has 14 positive and 16 negative targets. Activation AUROC is 0.775 [0.580, 0.921]; text is 0.766 [0.576, 0.907]. In the lexically exposed first-decision subset of 21 targets, AUROCs are 0.654 and 0.620, with difference 0.034 [−0.337, 0.334]. No clear advantage is established.

A separate source-comparable analysis follows the clarified board-plus-prior-edit contract, fits text on all 70 original training episodes, and uses the supplied probe scores. On the same 30 first-decision test points, AUROC is 0.837 for the probe, 0.786 for supplied board-only text, and 0.761 for board-plus-edits. The probe-minus-board-plus-edits difference is 0.076 [−0.049, 0.228]. This also does not establish a clear advantage. It reserves no validation set and reports no calibrated operating-point metrics. See [contract comparison](transcript_contract_comparison.md).

At the validation-selected first-decision threshold, the probe detects 8/14 positives and falsely alerts on 4/16 negatives. Realized test FPR is 25%, despite a 5% validation target. The text threshold is never-alert: limited validation calibration must not be confused with absent ranking signal.

In the pooled-threshold timing analysis, the probe gives two one-decision-early alerts, six imminent alerts and six misses among 14 positives, plus four false alerts among 16 negatives. Only three test positives permit an earlier decision. Third-decision evaluation has zero eligible targets.

Four real-data [figures and machine-readable results](isahan_analysis.md#figures-and-artifacts) are saved. Mock artifacts remain separately watermarked. The independent real ownership smokes produced 16 vectors, 12 LLM scores and no unauthorized attempts; these do not support fitting a binary predictor.

For the exploratory shared-state fanout transfer, the same frozen models reproduce their main predictions exactly before transfer. On 36 targets, activation AUROC is 0.305 and text 0.719. Only four positives across three parents make this a narrow out-of-distribution limitation, not a general result. See [transfer analysis](fanout_transfer.md).

## 9. Interpretation

The evidence supports a limited marker-compliance comparison. It does not establish unauthorized defection, intentions, objective adoption or recruitment spreading. Similar point estimates do not prove equivalence; the paired interval permits useful effects in either direction. The available timing largely tests imminent responses.

## 10. Limitations

Limitations include relaxed authorization, few positives, short traces, a previously analyzed test, repeated contexts across train/test, absent runtime provenance, and parser failures converted to `done`. Ten recipient parse failures, eight truncated, complicate interpreting negatives as resistance. The supplied board-only text model sees less than activation prefill. The LLM comparison is incomplete for this dataset.

Fanout recipients share state; four positives cluster in three parents, and no recipient posts a recruitment message. It requires parent-level uncertainty and provides no observed cascade. See [fanout audit](fanout_findings.md).

## 11. Ethical and dual-use considerations

All tasks use inert markers and synthetic file edits. No sensitive systems or data are targeted. Collaborator source and active infrastructure were not changed. Our separately provisioned A40 was stopped after backing up smoke artifacts; current analysis is CPU-only. Credentials remain outside downloadable artifacts.

## 12. Related work and next steps

The [related-work review](related_work.md) covers all requested sources. Pre-Crime motivates horizon separation and trained text controls; deception and sleeper probes motivate representation tests without proving recruitment generalization.

A new authorization experiment must retain an explicit boundary, verify attempted tool violations, freeze attacks after separate pilots, and collect fresh grouped data with earlier decisions. These policy and timing limitations should be central to the submission rather than hidden by favorable surrogate metrics. Reproduction commands are in the README.

## Coordinator-update checks

The [peer and replay note](replay_and_peer_claims.md) reproduces the stated 3/6 versus 5/67 marker-state counts and corrects the new-insertion risk set to 1/4 versus 3/65. Neither is causal evidence of peer pressure. Replay can reproduce same-model prefill states only with matched weights and exact tokenized context; local-model replay of an unverified remote model does not certify the remote internals. A proposed fanout replay-key patch is prepared separately for review.
