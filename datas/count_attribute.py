# count all dataset attribute(samples, features, labels) to all_attribute.csv

import pandas as pd


def get_attributes():
    fname = "selected_datasets.txt"
    attributes = None
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            dstype, dsname = line.split(":")
            dstype = dstype.strip()
            dsname = dsname.split()
            path = "%s/all_result/all_attribute.csv"%dstype
            df = pd.read_csv(path, index_col=0).ix[dsname]
            attributes = pd.concat((attributes, df))
    return attributes


def main():
    attributes = get_attributes()
    attributes.to_csv("all_attribute.csv")


if __name__ == "__main__":
    main()
