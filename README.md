
# gswnorm2021

Repository for the 2021 Shared Task on Text Normalization for Swiss German.
Further information and sign up form are on the 
[task website](https://sites.google.com/view/gswnorm2021).

## Content

```
gswnorm2021
|
|   README.md  # this readme file
|   requirements.txt  # requirements for this repository
|   evaluation.py  # evaluation script
|   baseline.py  # a very simple baseline model to compare against
```

## Data Formats

We distribute the training data as a *json* file. The file contains an array
with entries in the following format:

```json
{
  "sample_id": "some_uuid",
  "tokens": ["text", "in", "swiss", "german"],
  "annotation1": ["annotations", "for", "first", "annotator"],
  "annotation2": ["annotations", "for", "second", "annotator"]
}
```

You can assume that the fields *tokens*, *annotation1*, and *annotation2*
are of the same length.

We expect predictions to be another *json* file containing an array with entries
in the following format:
```json
{
  "sample_id": "some_uuid",
  "tokens": ["text", "in", "swiss", "german"],
  "prediction": ["your", "predictions", "for", "tokens"]
}
```
We will assume that the *tokens* and *prediction* fields are of the same length.

In general, if one token entry from a *tokens* field is to be normalized to
multiple tokens, they should be concatenated with a whitespace as separator.


## Evaluation

We will use the error reduction rate (ERR) [(van der Groot, 2019)](https://www.aclweb.org/anthology/P19-3032.pdf)
to assess your model's performance.
A single normalization prediction will be counted as correct if it matches one
of the two annotator's normalization.

To run the evaluation script, you will have to provide the paths to *json* files
containing the annotated data, as well as your predictions.

```bash
python -m evaluation --ann_path /path/to/data.json --predicted /path/to/predictions.json
```

ERR reductions measures how much a model improves accuracy compared to doing nothing,
i.e. copying all tokens from the input.

## Baseline

We provide a simple baseline model that predicts the most common normalization
in the training set for every token. The script will run 5 fold cross-validation
given the path to the training data. 

```bash
python -m baseline --data /path/to/train.json
```

Note that this model is slightly more sophisticated
than the simple copy-all baseline used to compute ERR.