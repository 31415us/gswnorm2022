
import json
import argparse
from collections import Counter


def check_duplicate_ids(data):
    id_counts = Counter(d['sample_id'] for d in data)
    duplicates = {
            sample_id for sample_id, count in id_counts.items() if count > 1}
    if len(duplicates) == 0:
        print("Found no duplicates.")
        return True
    else:
        print("Found duplicate ids:")
        for dup_id in duplicates:
            print(dup_id)
        return False


def check_overlap(test_data, pred_data):
    test_ids = {t['sample_id'] for t in test_data}
    pred_ids = {p['sample_id'] for p in pred_data}

    excessive_ids = pred_ids - test_ids  # ids in pred that are not in test
    missing_ids = test_ids - pred_ids  # ids in test that are not in pred

    err = len(excessive_ids) == len(missing_ids) == 0

    if len(excessive_ids) == 0:
        print("Found no excessive samples.")
    else:
        print("Found excessive samples:")
        for ex in excessive_ids:
            print(ex)

    if len(missing_ids) == 0:
        print("Found no missing samples.")
        for miss in missing_ids:
            print(miss)

    return err


def check_format(pred_data):
    for p in pred_data:
        id_ok = p.get('sample_id') is not None
        toks_ok = p.get('tokens') is not None
        pred_ok = p.get('prediction') is not None

        if not (id_ok and toks_ok and pred_ok):
            print("Make sure all your predictions contain the fields: ['sample_id', 'tokens', 'prediction']")
            return False

    print("Format of submission: ok (all necessary fields are present)")
    return True


def check_lengths(test_data, pred_data):
    pred_map = {
        d['sample_id']: d
        for d in pred_data
    }
    
    ok = True
    for t in test_data:
        length = len(t['tokens'])
        pred = pred_map.get(t['sample_id'])
        if pred is None:
            continue
        toks_ok = len(pred['tokens']) == length
        preds_ok = len(pred['prediction']) == length

        if not (toks_ok and preds_ok):
            print(f"Length of tokens or predicions don't match test data for sample {t['sample_id']}")
            ok = False
    if ok:
        print("Length of predictions match test data.")
    return ok


def main(test_path: str, pred_path: str):
    with open(test_path, 'r') as fin:
        test_samples = json.load(fin)

    with open(pred_path, 'r') as fin:
        pred_samples = json.load(fin)

    ok = check_format(pred_samples)
    if not ok:
        return

    ok = check_duplicate_ids(pred_samples)

    ok &= check_overlap(test_samples, pred_samples)

    ok &= check_lengths(test_samples, pred_samples)

    if ok:
        print("We found no obvious problem with your submission.")
    else:
        print("There seems to be a problem with your submission.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--test", dest="test_path", type=str, required=True)
    parser.add_argument(
        "-p", "--predicted", dest="pred_path", type=str, required=True)
    args = parser.parse_args()

    main(args.test_path, args.pred_path)
