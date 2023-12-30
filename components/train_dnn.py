import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # Add to make DNN module importable
import datetime
import fnmatch
from pathlib import Path
from DNN import Net, SigmoidNet, Net_10ReLU
import pandas as pd
import torch
from torch import optim
from torch import nn
from torch.autograd import Variable
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


LABEL_FEATURE_NAME = 'alive'

class ModelCoach:

    def __init__(self, model, optimizer, batch_size, learn_rate):
        self.model = model
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.learn_rate = learn_rate

    def train(self, data, labels, epoch):
        self.model.train()
        permutation = torch.randperm(data.size()[0])

        for i in range(0, data.shape[0], self.batch_size):
            indices = permutation[i:i+self.batch_size]
            batch_x, batch_y = data[indices], labels[indices]

            batch_data = Variable(batch_x)
            target = Variable(batch_y)

            self.optimizer.zero_grad()
            out = self.model(batch_data)

            criterion = nn.BCELoss()
            loss = criterion(out[:,0], target)
            loss.backward()
            self.optimizer.step()
            
            # Print progress
            prediciton = torch.round(out)
            correct = prediciton.eq(target.data.view_as(prediciton)).sum()

        if epoch % 100 == 0:
            print(str(loss) + str(correct/data.shape[0]))

    def test(self, data, labels):
        self.model.eval()
        data = Variable(data)
        out = self.model(data)[:, 0]
        prediction = torch.round(out)

        cm = confusion_matrix(labels, prediction.detach().cpu().numpy(), labels=[0, 1])
        return cm


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


def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")


def run(config):
    report("Commence training of dataset")

    torch.device(config.get('DEVICE', 'cpu'))
    
    epochs = config.get('EPOCHS')
    batch_size = config.get('BATCH_SIZE')
    learn_rate = config.get('LEARN_RATE')
    

    ipath = Path(config['INPUT_PATH'])
    opath = Path(config['OUTPUT_PATH'])
    artifact_name = config['ARTIFACT_NAME']

    df = pd.read_csv(ipath.joinpath(config['TRAIN_INPUT_FNAME'])).fillna(0)
    # Shuffle the data
    for _ in range(10):
        df = df.sample(frac=1).reset_index(drop=True)

    features = get_features(config.get('FEATURES'), df.columns.tolist())
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    
    train_data = torch.Tensor(df_train[features].to_numpy())
    train_labels = torch.Tensor(df_train[LABEL_FEATURE_NAME].to_numpy())
    test_data = torch.Tensor(df_test[features].to_numpy())
    test_labels = torch.Tensor(df_test[LABEL_FEATURE_NAME].to_numpy())

    model = Net(len(features))
    model.post_init()

    optimizer = optim.RMSprop(model.parameters(), lr=learn_rate)
    coach = ModelCoach(model, optimizer, batch_size, learn_rate)

    for epoch in range(epochs):
        if epoch % 100 == 0:
            report(f"Training model for epoch {epoch}/{epochs}")
        coach.train(train_data, train_labels, epoch)
        cm = coach.test(test_data, test_labels)

    print(cm)

    if not opath.exists():
        opath.mkdir(parents=True)

    model.save(opath)
    # Save traced model
    sm = torch.jit.script(model)
    sm.save(opath.joinpath(artifact_name))

    