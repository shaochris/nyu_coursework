# Risk Management System for Vehicle Leasing

# The reason to do this project:

One of the most important thing for vehicle company is how to make their asset safe. When customers try to cheat this company on purpose or can not afford the leasing fee anymore, the first thing for the company is making sure their vehicle is under control(locating the car and trying to get it back after). After doing some researches and reading papers, I find there isn’t any Risk Management System for Vehicle Leasing companies to predict or monitor customer behavior automatically or by the machine-learning way when customers already get the car. (Chinese Vehicle Leasing companies only use Credit score card system before deciding whether to sell a car to the customer.) In this way, I believe the project is a good and first try in China to do this.

# Data Resource

Because it’s an unprecedented system in China before, we collect as many kind of data as we could. The main four data resource is: 

1. Customer personal information data(from Chinese Vehicle Leasing company)

2. Customer credit information(from three large Chinese Big Data Credit Information Platform) 3. Repayment history data(from Chinese Vehicle Leasing company)

4. GPS alert/travel history(from two different GPS company)

After matching four kinds of data, we find the number of samples who has four features is 1213. We label these samples in many ways

1. label into three kinds: cheating on purpose(remove the GPS equipment or mortgage the vehicle to third company), can not pay for the monthly fee and return the vehicle and good customer(can do the successive payment/ maybe few days delay but paid)
2. combine the first two condition together as bad customer and second kind is good customers as before)

We did our project in the process below, which is also the process that we found lots of Chinese companies use for solving machine learning and big data problems.

Before dealing with data, the Risk Management Department of Leasing Company helps us refine the possibly useful features. There is the feature we selected to use in the below image, the specific form is also in the features.pdf file in the directory.

# Data Cleaning and collation:

We use codes with file name PayData to deal with repayment data, gpsData_juruiyun and gpsData_wanwei files to deal with data from two different GPS company separately, then, we use gatherGPS to put data from two different data source together. Finally, we use gatherData to put all four kinds of data together(Personal Information Data, Credit Information Data, GPS Alert/Travel History Data and Repayment History Data.)

## The Rule of Data picking:

We consider about a condition is that for the two kinds of bad customer, their data after their cheating happen or returning the vehicle back to the company is useless. So for the good customers, we choose the data of past 15 days before gathering these data, but for the bad customers, we choose to use the data 15 days before their breach of contract behavior happen(may be few days shift).

# Algorithm Choosing and Parameter Picking:

We choose three different kinds of algorithm which are Linear Regression, Decision Tree and Gradient Boosting Decision Tree(with or without SMOTE algorithm). Due to the number of sample is not that large and bad samples are much fewer than good customer samples, SMOTE algorithm could help us to deal with the Imbalanced class problem.

In the model building process, we also use cross-validation to test it, one hot encoder, weight of evidence and cross validation.

After trying different algorithms, we could find GBDT algorithm with SMOTE has the best effective. In this way, we write the auto_gbdt file to find out best parameters(such as n_estimators, max_depth, min_samples_split, min_samples_leaf) for us.

Rre file helps to print out the model result for specific customers to observe the distribution of correct and incorrect prediction of model.

# Testing the model result:

For our project, it’s a classification problem, we use AUC/ROC and KS to test our model and results.

![Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled.png](Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled.png)

For GBDT model

![Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%201.png](Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%201.png)

For Logic Regression model

## We also observe the feature contribution for the model, we could see some of the feature has very high feature contribution.

![Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%202.png](Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%202.png)

## For the model result we could see the SMOTE algorithm is very important for our data and model.

![Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%203.png](Risk%20Management%20System%20for%20Vehicle%20Leasing%20a50bab666dd3412cbd1da18150b548ca/Untitled%203.png)

The software we use is Spyder in the Anaconda, because it could run specific part of code and show the variables easily.
