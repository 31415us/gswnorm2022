
import json
import argparse
from evaluation import evaluate


class CountingBaseline:

    def __init__(self):
        self.normalization_counts = {}

    def train(self, train_data):
        for entry in train_data:
            for token, ann1, ann2 in zip(
                    entry['tokens'], entry['annotation1'], entry['annotation2']):
                if self.normalization_counts.get(token) is None:
                    self.normalization_counts[token] = {}

                self.normalization_counts[token][ann1] =\
                    self.normalization_counts[token].get(ann1, 0) + 1
                self.normalization_counts[token][ann2] = \
                    self.normalization_counts[token].get(ann2, 0) + 1

    def __prediction_entry(self, test_entry):
        return {
            "sample_id": test_entry['sample_id'],
            "tokens": test_entry['tokens'],
            "prediction": [
                max(
                    self.normalization_counts[token].keys(),
                    key=lambda k: self.normalization_counts[token][k]
                ) if self.normalization_counts.get(token) else token
                for token in test_entry['tokens']
            ]
        }

    def predict(self, test_data):
        return [
            self.__prediction_entry(e)
            for e in test_data
        ]


def training_loop(data, n_cv=5):
    fold_size = len(data) // n_cv
    errs = []
    fold_count = 0
    for start_ix in range(0, len(data), fold_size):
        test_ixs = set(range(start_ix, start_ix + fold_size))
        train_data = [d for ix, d in enumerate(data) if ix not in test_ixs]
        test_data = [d for ix, d in enumerate(data) if ix in test_ixs]

        model = CountingBaseline()
        model.train(train_data)
        predictions = model.predict(test_data)

        err = evaluate(test_data, predictions)
        print(f"ERR on fold {fold_count} is {err:.4f}")
        fold_count += 1
        errs.append(err)

    print(f"Average ERR {sum(errs) / len(errs):.4f}")


def main(data_path, n_cv=5):
    with open(data_path, 'r') as fin:
        data = json.load(fin)

    training_loop(data, n_cv=n_cv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data", dest="data_path", type=str, required=True)
    parser.add_argument(
        "-n", "--n_cv", dest="n_cv", type=int, default=5)
    args = parser.parse_args()

    main(args.data_path, args.n_cv)

