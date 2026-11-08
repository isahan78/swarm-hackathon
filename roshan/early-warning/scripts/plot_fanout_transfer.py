"""Plot the saved frozen transfer comparison without refitting any monitor."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main-results', required=True)
    parser.add_argument('--fanout-results', required=True)
    args = parser.parse_args()
    main_dir, fanout_dir = Path(args.main_results), Path(args.fanout_results)
    primary = json.loads((main_dir/'evaluation.json').read_text())['horizons']['step_1']['monitors']
    transfer = json.loads((fanout_dir/'evaluation.json').read_text())['horizons']['step_1']['monitors']
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for name, label, color, offset in [('activation', 'Activation probe', '#2166ac', -.10),
                                       ('text_tfidf', 'TF-IDF text classifier', '#b35806', .10)]:
        entries = [primary[name], transfer[name]]
        score = np.array([r['auroc'] for r in entries])
        ci = np.array([r['auroc_ci95'] for r in entries])
        ax.errorbar(np.array([0, 1])+offset, score,
            yerr=np.stack([score-ci[:, 0], ci[:, 1]-score]), fmt='o', capsize=5,
            markersize=7, color=color, label=label)
    ax.axhline(.5, color='.65', ls=':', lw=1)
    ax.set(xticks=[0, 1], xticklabels=['Two-agent frozen test\n30 parents; 14 positive targets',
        'Three-target shared-state fanout\n12 parents; 4 positive targets'],
        xlim=(-.5, 1.5), ylim=(0, 1), ylabel='First-decision AUROC',
        title='Frozen monitor transfer: marker-compliance prediction')
    ax.legend(frameon=False, loc='lower left')
    ax.spines[['top', 'right']].set_visible(False)
    fig.text(.5, .035, 'Outcome: marker insertion, not verified unauthorized behavior. Parent-bootstrap 95% intervals.\n'
        'Fanout is exploratory OOD transfer with shared state and only 3 positive parent episodes.',
        ha='center', fontsize=9)
    fig.subplots_adjust(bottom=.25, left=.10, right=.98, top=.88)
    for extension in ('png', 'svg'):
        fig.savefig(fanout_dir/f'figure_transfer.{extension}', dpi=200)
    plt.close(fig)


if __name__ == '__main__':
    main()
