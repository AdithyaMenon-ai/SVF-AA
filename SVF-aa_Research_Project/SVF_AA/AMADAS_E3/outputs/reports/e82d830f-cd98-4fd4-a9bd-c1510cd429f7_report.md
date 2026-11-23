# Iris Dataset Analysis Report

## Objective
The objective of this analysis is to perform a comprehensive data analysis on the Iris dataset and build a classification model to predict the species of Iris flowers based on their sepal and petal measurements.

## Dataset
The Iris dataset contains measurements of sepal length, sepal width, petal length, and petal width for three species of Iris flowers. The target variable indicates the species of the Iris flower.

## Cleaning
- **Original Rows:** 150
- **Cleaned Rows:** 149 (1 duplicate row removed)
- **Columns:** 5
- **Missing Values:** None in any column before or after cleaning
- **Rows with Missing Target Values Removed:** 0

The dataset was cleaned to remove one duplicate row, ensuring the integrity of the dataset for model training.

## EDA
- **Distributions:** Visualized using histograms to understand the distribution of each feature.
- **Correlations:** Correlation matrix to identify the relationships between features.

## Machine Learning
- **Task:** Classification
- **Model:** Logistic Regression
- **Training Rows:** 119
- **Test Rows:** 30
- **Metrics:**
  - **Accuracy:** 0.9333
  - **F1-Weighted:** 0.9333

The Logistic Regression model was successfully trained on 119 rows of the dataset, achieving an accuracy and F1-weighted score of 93.33%, suggesting the model performs well on the classification task.

## Insights
1. **Dataset Integrity:** The Iris dataset contains 149 samples, with no missing values, making it suitable for analysis.
2. **Feature Correlation:** The features 'sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', and 'petal width (cm)' are highly correlated with the target variable, indicating strong predictive power for classification tasks.
3. **Model Performance:** A Logistic Regression model was successfully trained on 119 rows of the dataset, achieving an accuracy and F1-weighted score of 93.33%, suggesting the model performs well on the classification task.
4. **Data Cleaning:** The dataset cleaning process was thorough, removing only one duplicate row, and no rows were removed due to missing target values, ensuring the integrity of the dataset for model training.

## Limitations
- **Model Choice:** The Logistic Regression model was chosen for simplicity and interpretability. Other models such as Random Forest or Support Vector Machines could potentially provide better performance.
- **Feature Engineering:** No feature engineering was performed, which could potentially improve model performance.
- **Cross-Validation:** No cross-validation was performed, which could provide a more robust estimate of model performance.

## Artifacts
- **Plots:**
  - Distributions: `outputs\\plots\\e82d830f-cd98-4fd4-a9bd-c1510cd429f7\\distributions.png`
  - Correlations: `outputs\\plots\\e82d830f-cd98-4fd4-a9bd-c1510cd429f7\\correlations.png`

## Skipped ML Tasks
- **Feature Importance:** Not computed as part of the analysis.
- **Confusion Matrix:** Not provided in the results.
- **Classification Report (Precision, Recall, F1-score):** Not provided in the results.

This report provides a comprehensive overview of the analysis and model training process for the Iris dataset.