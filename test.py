def pthFactor(n,p):
    factor = 0
    for i in range(1,n+1):
        if n % i == 0:
            factor = i
            p = p - 1
        if p <= 0:
            break
    if p>0:
        return 0
    return factor
print(pthFactor(22876792454961,28))