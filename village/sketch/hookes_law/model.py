# 场景：胡克定律

# 实验数据

data = [
    [ 20.0, 3.0 ],
    [ 40.0, 7.0 ],
    [ 60.0, 10.0 ],
    [ 80.0, 13.0 ],
    [ 100.0, 16.0 ]
]

# 直觉，实验应当满足的关系式：Δl = km

# 最小二乘法线性拟合，求 k
def hookes_fit(data):
    Σx = Σy = Σxy = Σxx = 0.0
    N = len(data) + 1
    
    for datum in data:
        x = datum[0]
        y = datum[1]
        
        Σx += x
        Σy += y
        Σxy += (x * y)
        Σxx += (x * x)
    
    xbar = Σx / N
    ybar = Σy / N
    k = (Σxy - (N * xbar * ybar)) / (Σxx - (N * xbar * xbar))
    # b = ybar - (k * xbar)
    
    return k

print(f"k = {hookes_fit(data)}")
