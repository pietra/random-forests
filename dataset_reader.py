import pandas


def read_dataset(dataset_name):
    dataset_path = "datasets/" + dataset_name
    dataset = pandas.read_csv(dataset_path)
    attributes = dataset.columns.values.tolist()
    return dataset, attributes
