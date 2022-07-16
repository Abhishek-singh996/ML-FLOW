import mlflow

def cal_nth_root(x,n):
    return x**n

if __name__=="__main__":
    with mlflow.start_run():
        x, n = 2, 5
        y = cal_nth_root(x,n)
        mlflow.log_param('x',x)
        mlflow.log_param('n',n)
        mlflow.log_metric('y',y)
