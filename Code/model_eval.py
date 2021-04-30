import numpy as np
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

def residual_diagnostics(f, a, model):
    f.suptitle("RESIDUAL DIAGNOSTICS", fontsize = 17)
    sns.histplot(model.resid, ax = a[0])
    a[0].set_xlabel("Model Residuals", fontsize = 15)
    a[0].set_title("Distribution of Model Residuals", fontsize = 16);

    sm.qqplot(model.resid, line = "45", fit = True, ax = a[1]);
    a[1].set_xlabel("Theoretical Quantiles", fontsize = 15);
    a[1].set_title("QQ Plot of Model Residuals", fontsize = 16);
    a[1].set_ylabel("Sample Quantiles", fontsize = 15);

    sns.scatterplot(x = model.fittedvalues, y = model.resid, ax = a[2])
    a[2].set_xlabel("Fitted Values", fontsize = 15)
    a[2].set_ylabel("Model Residuals", fontsize = 15)
    a[2].set_title("Residuals vs. Fitted Values", fontsize = 16);

    f.tight_layout()

def CV_RMSE(df, resp, num_folds = 5, squared = False):
    # define response and predictor variables
    y = df[resp]
    X = df.drop(resp, axis = 1)

    # initialise lists to store RMSE per fold
    train_RMSEs = []
    test_RMSEs = []

    kfold = KFold(num_folds)

    for train, test in kfold.split(df):
        # define training and test data
        X_train = X.iloc[train,:]
        X_test = X.iloc[test,:]
        y_train = y.iloc[train]
        y_test = y.iloc[test]
        # fit model with training data
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        # calculate training and test predictions
        y_hat_train = lr.predict(X_train)
        y_hat_test = lr.predict(X_test)
        if squared:
            train_mse = mean_squared_error(np.sqrt(y_train), np.sqrt(y_hat_train))
            test_mse = mean_squared_error(np.sqrt(y_test), np.sqrt(y_hat_test))
        else:
            train_mse = mean_squared_error(y_train, y_hat_train)
            test_mse = mean_squared_error(y_test, y_hat_test)
        # store RMSEs for current fold
        train_RMSEs.append(np.sqrt(train_mse))
        test_RMSEs.append(np.sqrt(test_mse))
    
    train_RMSE = np.mean(train_RMSEs)
    test_RMSE = np.mean(test_RMSEs)

    return train_RMSE, test_RMSE

def visualise_results(results, fig, axes):
    hist_dict = results.history
    x = range(len(hist_dict["loss"]))
    sns.lineplot(x = x, y = hist_dict["loss"], ax = axes[0])
    sns.lineplot(x = x, y = hist_dict["val_loss"], ax = axes[0])
    axes[0].legend(["loss", "val_loss"])
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epochs")
    axes[0].set_ylabel("Loss")

    sns.lineplot(x = x, y = hist_dict["acc"], ax = axes[1])
    sns.lineplot(x = x, y = hist_dict["val_acc"], ax = axes[1])
    axes[1].legend(["acc", "val_acc"])
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epochs")
    axes[1].set_ylabel("Accuracy")

    fig.tight_layout()