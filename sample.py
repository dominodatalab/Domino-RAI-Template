import pandas as pd

def split_label(dataset, target_feature):
    X = dataset.drop([target_feature], axis=1)
    y = dataset[[target_feature]]
    return X, y


target_feature = 'income'
test_data = pd.read_csv('./adult-test.csv', skipinitialspace=True)
X_test_original, y_test = split_label(test_data, target_feature)

test_data_sample = test_data.sample(n=100, random_state=5)

# Create a new column with 2 to 3 unique values ; replace with numbers if needed
#unique_values = ['Private', 'Local-gov', 'State-gov']  # Replace with your desired unique values
#test_data_sample['workclass'] = unique_values[:len(test_data_sample)]

# Write the DataFrame back to a CSV file
test_data_sample.to_csv('./adult-test-sample.csv')
