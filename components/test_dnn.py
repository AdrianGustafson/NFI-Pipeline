import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # Add to make DNN module importable
import fnmatch
import datetime
from pathlib import Path
from DNN import Net, SigmoidNet, Net_10ReLU
import pandas as pd
import numpy as np
import torch
from torch import nn
from torch.autograd import Variable
from sklearn.metrics import (confusion_matrix, classification_report, ConfusionMatrixDisplay,
    precision_recall_curve
)
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")


def get_features(feature_list, columns):
    """Utility function to expand wildcard features in the list, e.g., used for species
    
    """
    res = []
    for feature in feature_list:
        if '*' in feature:
            matches = fnmatch.filter(columns, feature)
            res.extend(matches)
        else:
            res.append(feature)
    return res


def run(config):
    report("Producing test scores and plots for DNN")

    ipath = Path(config['INPUT_PATH'])
    opath = Path(config['OUTPUT_PATH'])
    test_data_fname = Path(config['TEST_DATA_FNAME'])

    test_data = pd.read_csv(ipath.joinpath(test_data_fname)).fillna(0)
    features = get_features(config['FEATURES'], test_data.columns)
    device = torch.device(config.get('DEVICE', 'cpu'))
    state_path = config['STATE_PATH']
    model = Net(len(features))
    model.load_state_dict(torch.load(state_path, map_location=device))

    
    test_input = torch.Tensor(test_data[features].to_numpy())
    test_labels = torch.Tensor(test_data['alive'].to_numpy(int))

    model.eval()

    data = Variable(test_input)
    pred = model(data)[:, 0]
    pred_binary = torch.round(pred).detach()
    # Prepare output
    if not opath.exists():
        opath.mkdir(parents=True)

    # Write the classification report
    f1 = classification_report(test_labels, pred_binary)
    with open(opath.joinpath('f1-report.txt'), 'w') as fh:
        fh.write(f1)

    # Precision-recall curve
    precisions, recalls, thresholds = precision_recall_curve(test_labels, pred.detach().numpy())

    # Threshold curve
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(thresholds, precisions[:-1], 'b--', label='Precision', linewidth=2)
    ax.plot(thresholds, recalls[:-1], 'g-', label='Recall', linewidth=2)

    ax.set_xlabel('Threshold')
    ax.set_ylabel('Precision/Recall')
    ax.grid(True, 'major')
    ax.legend(loc='center left')

    fig.savefig(opath.joinpath('precision-recall-threshold_curve.png'))

    # Precision/Recall curve
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(recalls, precisions, 'b-', label='Precision/Recall curce', linewidth=2)

    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.grid(True, 'major')
    ax.legend(loc='center right')
    ax.set_ylim(0.85,1)
    ax.set_xlim(0,1)
    ax.add_line(Line2D([1, 0], [0.85, 1], linestyle='--', color='k'))
    fig.savefig(opath.joinpath('precision-recall_curve.png'))


    for cutoff in (0.20, 0.50, 0.80):
        find_cutoff = lambda x: 0 if x < cutoff else 1
        pred_cutoff = np.array([find_cutoff(v) for v in pred])

        fig, ax = plt.subplots(1,2, figsize=(12,6))
        cm = confusion_matrix(test_labels.numpy(), pred_cutoff)
        cmdisp = ConfusionMatrixDisplay(cm, display_labels=['Dead', 'Alive'])
        cmdisp.plot(ax=ax[0])
        ax[0].set_title('Absolute values')
        
        cmdisp_rel = ConfusionMatrixDisplay.from_predictions(
            test_labels.numpy(), pred_cutoff,
            normalize="true", values_format='.0%',
            display_labels=['Dead', 'Alive'])
        cmdisp_rel.plot(ax=ax[1])
        ax[1].set_title('Relative to total in category')
        fig.suptitle(f'Threshold: {cutoff}')
        fig.savefig(opath.joinpath(f'confusion_matrix_{cutoff}_cutoff.png'))

