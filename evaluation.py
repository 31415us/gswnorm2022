
import json
import argparse


def baseline_predictions(annotated):
    return [
        {
            "sample_id": entry['sample_id'],
            "tokens": entry['tokens'],
            "prediction": entry['tokens'],
        }
        for entry in annotated
    ]


def accuracy(annotated, predicted):
    annotation_map = {
        entry['sample_id']: entry
        for entry in annotated
    }
    correct = 0
    total = 0
    for entry in predicted:
        annotation_entry = annotation_map[entry['sample_id']]

        for ix, prediction in enumerate(entry['prediction']):
            ann1 = annotation_entry['annotation1'][ix]
            ann2 = annotation_entry['annotation2'][ix]

            if prediction == ann1 or prediction == ann2:
                correct += 1
            total += 1

    return correct / total


def evaluate(annotated, predicted):
    baseline_predicted = baseline_predictions(annotated)
    baseline_accuracy = accuracy(annotated, baseline_predicted)
    system_accuracy = accuracy(annotated, predicted)

    err = (system_accuracy - baseline_accuracy) / (1. - baseline_accuracy)
    return err, system_accuracy


def main(annotated_path: str, predicted_path: str):
    with open(annotated_path, 'r') as fin:
        annotated = json.load(fin)

    with open(predicted_path, 'r') as fin:
        predicted = json.load(fin)

    error_reduction, sys_acc = evaluate(annotated, predicted)

    print(f"SYSTEM ACCURACY: {sys_acc:.4f}")
    print(f"ERROR REDUCTION RATE: {error_reduction:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--annotated", dest="ann_path", type=str, required=True)
    parser.add_argument(
        "-p", "--predicted", dest="pred_path", type=str, required=True)
    args = parser.parse_args()

    main(args.ann_path, args.pred_path)
