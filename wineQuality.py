import numpy as np
import pandas as pd
from time import time
from IPython.display import display

import matplotlib.pyplot as plt
import seaborn as sns

# Import supplementary visualization code visuals.py from project root folder
import visuals as vs


data = pd.read_csv("data/winequality-red.csv", sep=';')
display(data.head(n=5))

data.isnull().any()


data.info()


# Total number of wines
n_wines = data.shape[0]

# Number of wines with quality rating above 6
quality_above_6 = data.loc[(data['quality'] > 6)]
n_above_6 = quality_above_6.shape[0]

quality_below_5 = data.loc[(data['quality'] < 5)]
n_below_5 = quality_below_5.shape[0]

quality_between_5 = data.loc[(data['quality'] >= 5) & (data['quality'] <= 6)]
n_between_5 = quality_between_5.shape[0]

# Percentage of wines with quality rating above 6
greater_percent = (n_above_6 * 100)/n_wines


print("Total number of wine data: {}".format(n_wines))
print("Wines with rating 7 and above: {}".format(n_above_6))
print("Wines with rating less than 5: {}".format(n_below_5))
print("Wines with rating 5 and 6: {}".format(n_between_5))
print("Percentage of wines with quality 7 and above: {:.2f}%".format(greater_percent))

display(np.round(data.describe()))

vs.distribution(data, "quality")

display(np.round(data.describe()))


pd.plotting.scatter_matrix(data, alpha = 0.3, figsize = (40, 40), diagonal = 'kde')


correlation = data.corr()
plt.figure(figsize = (14, 12))
heatmap = sns.heatmap(correlation, annot = True, linewidths = 0, vmin = -1, cmap = "RdBu_r")



fixedAcidity_pH = data[['pH', 'fixed acidity']]


gridA = sns.JointGrid(x="fixed acidity", y="pH", data=fixedAcidity_pH)


gridA = gridA.plot_joint(sns.regplot, scatter_kws={"s": 10})


gridA = gridA.plot_marginals(sns.distplot)



fixedAcidity_citricAcid = data[['citric acid', 'fixed acidity']]
g = sns.JointGrid(x = "fixed acidity", y = "citric acid", data = fixedAcidity_citricAcid)
g = g.plot_joint(sns.regplot, scatter_kws = {"s"  : 10})
g = g.plot_marginals(sns.distplot)



fixedAcidity_density = data[['density', 'fixed acidity']]
gridB = sns.JointGrid(x="fixed acidity", y="density", data=fixedAcidity_density)
gridB = gridB.plot_joint(sns.regplot, scatter_kws={"s": 10})
gridB = gridB.plot_marginals(sns.distplot)



volatileAcidity_quality = data[['quality', 'volatile acidity']]
g = sns.JointGrid(x="volatile acidity", y="quality", data=volatileAcidity_quality)
g = g.plot_joint(sns.regplot, scatter_kws={"s": 10})
g = g.plot_marginals(sns.distplot)




fig, axs = plt.subplots(ncols=1,figsize=(10,6))
sns.barplot(x='quality', y='volatile acidity', data=volatileAcidity_quality, ax=axs)
plt.title('quality VS volatile acidity')

plt.tight_layout()
plt.show()
plt.gcf().clear()


quality_alcohol = data[['alcohol', 'quality']]

g = sns.JointGrid(x="alcohol", y="quality", data=quality_alcohol)
g = g.plot_joint(sns.regplot, scatter_kws={"s": 10})
g = g.plot_marginals(sns.distplot)


fig, axs = plt.subplots(ncols=1,figsize=(10,6))
sns.barplot(x='quality', y='alcohol', data=quality_alcohol, ax=axs)
plt.title('quality VS alcohol')

plt.tight_layout()
plt.show()
plt.gcf().clear()


fig, axs = plt.subplots(ncols = 1, figsize = (10, 6))
sns.barplot(x='fixed acidity', y='citric acid', data = fixedAcidity_citricAcid, ax = axs)
plt.title('fixed acidity VS citric acid')

plt.tight_layout()
plt.show()
plt.gcf().clear()



for feature in data.keys():
    Q1 = np.percentile(data[feature], q = 25)
    Q3 = np.percentile(data[feature], q = 75)
    interquartile_range = Q3 - Q1
    step = 1.5 * interquartile_range
    print("Data points considered outliers for the feature '{}':".format(feature))
    display(data[~((data[feature] >= Q1 - step) & (data[feature] <= Q3 + step))])
    outliers = []
    good_data = data.drop(data.index[outliers]).reset_index(drop = True)


"""
For our purposes, all wines with ratings less than 5 will fall under 0 (poor) category,
wines with ratings 5 and 6 will be classified with the value 1 (average), 
and wines with 7 and above will be of great quality (2).
"""
bins = [1, 4, 6, 10]
quality_labels = [0, 1, 2]
data['quality_categorical'] = pd.cut(data['quality'], bins = bins, labels = quality_labels, include_lowest = True)
display(data.head(n = 2))

#Data split into features and target label
quality_raw = data['quality_categorical']
features_raw = data.drop(['quality', 'quality_categorical'], axis = 1)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(features_raw, quality_raw, test_size = 0.2, random_state = 0)

print("Training set has {} samples".format(X_train.shape[0]))
print("Testing set has {} samples.".format(X_test.shape[0]))



from sklearn.metrics import fbeta_score
from sklearn.metrics import accuracy_score

def train_predict_evaluate(learner, sample_size, X_train, y_train, X_test, y_test): 
    """
    inputs:
       - learner: the learning algorithm to be trained and predicted on
       - sample_size: the size of samples (number) to be drawn from training set
       - X_train: features training set
       - y_train: quality training set
       - X_test: features testing set
       - y_test: quality testing set
    """

    results = {}
    
    """
    Fit/train the learner to the training data using slicing with 'sample_size' 
    using .fit(training_features[:], training_labels[:])
    """
    start = time()
    learner = learner.fit(X_train[:sample_size], y_train[:sample_size])
    end = time()
    

    results['train_time'] = end - start
    
    """
    Get the predictions on the first 300 training samples(X_train), 
    and also predictions on the test set(X_test) using .predict()
    """
    start = time() #
    predictions_train = learner.predict(X_train[:300])
    predictions_test = learner.predict(X_test)
    
    end = time()

    results['pred_time'] = end - start
            

    results['acc_train'] = accuracy_score(y_train[:300], predictions_train)
        

    results['acc_test'] = accuracy_score(y_test, predictions_test)
    

    results['f_train'] = fbeta_score(y_train[:300], predictions_train, beta=0.5, average='micro')
        

    results['f_test'] = fbeta_score(y_test, predictions_test, beta=0.5, average='micro')
       

    print("{} trained on {} samples.".format(learner.__class__.__name__, sample_size))
        

    return results



from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression


clf_A = GaussianNB()
clf_B = DecisionTreeClassifier(max_depth=None, random_state=None)
clf_C = RandomForestClassifier(max_depth=None, random_state=None)




samples_100 = len(y_train)
samples_10 = int(len(y_train)*10/100)
samples_1 = int(len(y_train)*1/100)


results = {}
for clf in [clf_A, clf_B, clf_C]:
    clf_name = clf.__class__.__name__
    results[clf_name] = {}
    for i, samples in enumerate([samples_1, samples_10, samples_100]):
        results[clf_name][i] = \
        train_predict_evaluate(clf, samples, X_train, y_train, X_test, y_test)

print(results)


vs.visualize_classification_performance(results)



model = RandomForestClassifier(max_depth=None, random_state=None)


model = model.fit(X_train, y_train)


importances = model.feature_importances_

print(X_train.columns)
print(importances)

# Plot
vs.feature_plot(importances, X_train, y_train)


from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer


clf = RandomForestClassifier(max_depth=None, random_state=None)



"""
n_estimators: Number of trees in the forest
max_features: The number of features to consider when looking for the best split
max_depth: The maximum depth of the tree
"""
parameters = {'n_estimators': [10, 20, 30], 'max_features':[3,4,5, None], 'max_depth': [5,6,7, None]}


scorer = make_scorer(fbeta_score, beta=0.5, average="micro")


grid_obj = GridSearchCV(clf, parameters, scoring=scorer)


grid_fit = grid_obj.fit(X_train, y_train)


best_clf = grid_fit.best_estimator_


predictions = (clf.fit(X_train, y_train)).predict(X_test)
best_predictions = best_clf.predict(X_test)


print("Unoptimized model\n------")
print("Accuracy score on testing data: {:.4f}".format(accuracy_score(y_test, predictions)))
print("F-score on testing data: {:.4f}".format(fbeta_score(y_test, predictions, beta = 0.5, average="micro")))
print("\nOptimized Model\n------")
print(best_clf)
print("\nFinal accuracy score on the testing data: {:.4f}".format(accuracy_score(y_test, best_predictions)))
print("Final F-score on the testing data: {:.4f}".format(fbeta_score(y_test, best_predictions, beta = 0.5,  average="micro")))


"""Give inputs in this order: fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide,
total sulfur dioxide, density, pH, sulphates, alcohol

"""
wine_data = [[8, 0.2, 0.16, 1.8, 0.065, 3, 16, 0.9962, 3.42, 0.92, 9.5],
            [8, 0, 0.16, 1.8, 65, 3, 16, 0.787, 0.1, 0.92, 1 ],
            [7.4, 2, 0.00, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 0.6]]
               

for i, quality in enumerate(best_clf.predict(wine_data)):
    print("Predicted quality for Wine {} is: {}".format(i+1, quality))

