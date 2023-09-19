## Origins of the Data

```Explain where the data was sourced from, transformations applied, PII / sensitive field obfuscation```

``` Explain the schema of the dataset. See example below ```
***
**Output** : `income` (binary classification <50k or >=50k)
***
**Inputs** :
 * `age` (age of the census participant)
 * `workclass` (professional affiliation)
 * `education` (highest level of education)
 * `marital status` (single, married, or divorced)
 * `occupation` (primary profession)
 * `relationship` (participant's role as a member of a family)
 * `race` (racial category)
 * `gender` (gender)
 * `capital gain` (net capital gain - annual)
 * `capital loss` (net capital loss - annual)
 * `hours per week` (hours employed per week)
 * `native country` (country of birth)
***
    

### Relevant research
``` Link any research papers and in-house projects referenced ```

## Model Performance & Analysis

### [Accuracy]
``` Publish all accuracy metrics during training ```

### [Probability Distributions]
``` If available, share the probability distributions of the datasets ```

#### Feature importances
![Feature Importance](https://github.com/vsridhar-ddl/Rev4Chapter3/blob/main/Income%20Pred%20Feature%20Importance.png?raw=true)
