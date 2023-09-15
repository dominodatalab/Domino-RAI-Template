import pandas as pd
import requests

#model_url = "https://rev4demo12597.product-team-sandbox.domino.tech:443/models/645d2a8155d999335fadfda1/latest/model"
#model_url = "https://rev4demo13502.dmo-team-sandbox.domino.tech:443/models/646952c7ea310c11d616c368/latest/model"
model_url = "https://rev4demo12597.product-team-sandbox.domino.tech:443/models/645d2a8155d999335fadfda1/latest/model"
rev12597_auth="Mg5UH7wej3hIglrIpJDvgoKOcaNSowZ0RQ3hLcYs5rmkNo0Twsd8VG7OdLdP95uH"
rev12502_auth="cJIbTdvI2O1APB11V42XkPK1WuAV2KPyWs6c3NY3BR98CWwVcAG5MMhp9kfBqcIV"


def split_label(dataset, target_feature):
    X = dataset.drop([target_feature], axis=1)
    y = dataset[[target_feature]]
    return X, y


target_feature = 'income'
test_data_sample = pd.read_csv('./adult-test-sample.csv', skipinitialspace=True)
#test_data = pd.read_csv('./adult-test.csv', skipinitialspace=True)
#test_data_sample = test_data.sample(n=1, random_state=5)

X_test_original, y_test = split_label(test_data_sample, target_feature)
X_test_dict = X_test_original.to_dict(orient='records')

features = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "gender",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country"
]


for record in X_test_dict:
    vals_list = list(record.values())
    vals_list.pop(0)
    send_record = dict(zip(features, vals_list))
    if (send_record['workclass'] == 'Self-emp-not-inc'):
            send_record['workclass'] = 'Local-gov'

    if(send_record['workclass'] == 'Self-emp-inc'):
            send_record['workclass'] = 'Federal-gov'

    response = requests.post(model_url,
         auth=(
             rev12597_auth,
             rev12597_auth
        ),
        json={"data":send_record}
    )
    #print(send_record)
    print(response.status_code)
    #print(response.headers)
    #print(response.json())
