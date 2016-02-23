def a():
    print 'a executed'
    return []

def b(x=a()):
    x.append(5)
    x.append(1)
    print x

if __name__ == '__main__':

    b()
    b()
    b()
