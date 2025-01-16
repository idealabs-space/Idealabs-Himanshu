
# Understanding Vertex AI AutoML: A Simple Guide

Vertex AI AutoML is a tool from Google Cloud that allows you to create machine learning models without needing to code. To understand how it works, let's break down the steps from the start of getting an input file to the final prediction. We'll also cover key concepts like types of machine learning, clean data requirements, and more.

---

## Step 1: Input File Preparation

### What happens?

You begin by uploading your data file to Vertex AI. This file could be a spreadsheet or a database export containing the information you want to analyze.

### Why is this step needed?

Without data, there's nothing for the machine learning model to learn from. The data is the foundation of any prediction or analysis.

### Example:

Imagine you run a clothing store and want to predict sales. Your input file might include columns like:

- Date
- Item type
- Price
- Quantity sold

---

## Step 2: Data Cleaning

### What happens?

The data is checked for errors, missing values, or inconsistencies. This step ensures the data is ready to be understood by the machine learning model.

### Why is this step needed?

Dirty data can confuse the model and lead to incorrect predictions. Clean data makes the model more accurate.

### What is Clean Data?

- **Consistent formats:** All dates in the same format, e.g., `YYYY-MM-DD`.
- **No missing values:** Columns like "Price" shouldn't have blanks.
- **No duplicates:** Remove repeated rows.
- **Correct labels:** If a column says "Yes/No," ensure it only contains those values.

### Example of Dirty Data:

- Typos: "Shirt" vs. "Shrit"
- Missing values: Price = blank
- Outliers: Quantity sold = 1,000,000 (when most values are under 100)

---

## Step 3: Selecting the Type of Machine Learning

### What happens?

You decide what kind of problem you're solving. Vertex AI supports these common types:

- **Regression:** Predicting a number (e.g., sales, temperature).
- **Classification:** Categorizing things (e.g., spam vs. not spam).
- **Forecasting:** Predicting future trends (e.g., sales over the next month).
- **Image Classification:** Identifying objects in pictures.
- **Text Analysis:** Understanding customer reviews.

### Why is this step needed?

Each type of problem requires a different approach. Choosing the right type helps Vertex AI design the correct model for your data.

---

## Step 4: Splitting the Data

### What happens?

The data is divided into three parts:

- **Training data:** Used to teach the model.
- **Validation data:** Used to fine-tune the model.
- **Test data:** Used to check how well the model performs.

### Why is this step needed?

Splitting the data ensures the model doesn't just memorize the data but learns patterns that can apply to new situations.

### Example:

If your file has 1,000 rows:

- 70% (700 rows) for training
- 15% (150 rows) for validation
- 15% (150 rows) for testing

---

## Step 5: Training the Model

### What happens?

Vertex AI uses the training data to learn patterns. For example, it might learn that higher prices generally lead to fewer sales. The training process involves applying specific algorithms to find the best-fit relationships in the data. Algorithms like decision trees, linear regression, or neural networks might be used, depending on the type of problem.

### Solved Questions with Detailed Math

#### Linear Regression: Predicting Test Scores

1. **Given Dataset:**

   - Hours Studied: [2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10]
   - Test Scores: [65, 67, 75, 73, 78, 82, 85, 88, 90, 93]

2. **Calculate Means:**

   - Mean of Hours (X̄): 5.85
   - Mean of Scores (Ȳ): 79.6

3. **Calculate Slope (m):**

   ```
   m = sum((X - X̄)(Y - Ȳ)) / sum((X - X̄)²)
   ```

   Numerator: sum((X - X̄)(Y - Ȳ)) = 132.625
   Denominator: sum((X - X̄)²) = 36.75

   ```
   m = 132.625/36.75 = 3.6098
   ```

4. **Calculate Intercept (c):**

   ```
   c = Ȳ - m · X̄
   c = 79.6 - (3.6098 × 5.85) = 58.4825
   ```

5. **Final Equation:**

   ```
   Test Score = 3.61 × Hours Studied + 58.48
   ```

6. **Predictions:**
   Predicted scores for given hours: [65.7, 69.3, 72.9, 74.7, 76.5, 80.1, 83.8, 87.4, 91.0, 94.6]

---

## Step 6: Evaluating the Model

### What happens?

The model is tested using the test data. Vertex AI shows you metrics like accuracy, precision, or error rate. Additionally, hyperparameter tuning is often performed during this phase.

### Hyperparameter Tuning

#### What is it?
Hyperparameters are settings that influence how the model learns, such as learning rate, batch size, or number of layers in a neural network. Unlike model parameters, hyperparameters are set before training and are not learned from the data.

#### Why is it important?
Tuning hyperparameters can significantly improve a model's performance. Vertex AI AutoML often automates this process, trying different combinations of hyperparameters to find the best setup.

#### Example:
For a neural network:
- Learning rate: How fast the model learns.
- Number of layers: Depth of the network.
- Batch size: Number of examples processed at once.

Vertex AI uses validation data to evaluate different hyperparameter combinations and selects the configuration that minimizes error or maximizes accuracy.

### Why is this step needed?
Evaluation ensures the model is reliable and not guessing randomly.

### Example:
For sales predictions:
- If actual sales were $100 and the model predicted $98, it's accurate.
- If the prediction was $500, the model needs improvement.

---

## Step 7: Making Predictions

### What happens?

You upload new data, and the model predicts the outcome. For example, you input product details, and the model predicts sales.

### Why is this step needed?

This is the ultimate goal—using the model to make informed decisions.

### Example:

Input: A new product priced at $20
Prediction: 150 units sold

---

## Summary

By following these steps, Vertex AI AutoML simplifies machine learning. It handles complex calculations behind the scenes, but understanding these steps ensures you know what's happening and why each part is important.
