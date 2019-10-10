import pandas


def read_dataset(dataset_path):
    dataset = pandas.read_csv(dataset_path)
    attributes = dataset.columns.values.tolist()
    attributes.remove('class')
    return dataset, attributes
