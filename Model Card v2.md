## About

```The data was extracted from the 1994 Census bureau database by Ronny Kohavi and Barry Becker (Data Mining and Visualization, Silicon Graphics). Records were extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1) && (HRSWK>0)). The objective is to classify a surveyed member of the census for income above $50K.```


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
Ron Kohavi, [Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid](http://robotics.stanford.edu/~ronnyk/nbtree.pdf), Proceedings of the Second International Conference on Knowledge Discovery and Data Mining, 1996. (PDF)


## Model Performance & Analysis

### [Responsible AI Dashboard](https://rev4demo12597.product-team-sandbox.domino.tech/modelproducts/6461635126cd6979a0457257)
*generated using the Responsible AI Project hosted at [RAI-github](https://github.com/microsoft/responsible-ai-toolbox/blob/main/LICENSE)*

#### Performance Metrics
![Performance Metrics](https://github.com/vsridhar-ddl/Rev4Chapter3/blob/main/Accuracy%20Scores.png?raw=true)

#### Probability Distributions
![Probability Distributions](https://github.com/vsridhar-ddl/Rev4Chapter3/blob/main/Census%20Data%20Prob%20Distribution.png?raw=true) 

#### Feature importances
![Feature Importance](https://github.com/vsridhar-ddl/Rev4Chapter3/blob/main/Income%20Pred%20Feature%20Importance.png?raw=true)
