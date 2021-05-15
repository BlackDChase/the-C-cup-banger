import csv
import math
import pprint


def get_nn():
    """
    Extracts data from the from the file into numpy arrays
    """
    with open('back.csv') as fl:
        XY = csv.reader(fl, delimiter=',')
        layers = []
        for row in XY:
            layers.append(list(row))
        return layers[0], layers[1:-1], layers[-1]


def get_desc(inpL, hiddenL, outpL):
    """
    Extracts data from the from the file into numpy arrays
    """
    with open('back_desc.csv') as fl:
        XY = csv.reader(fl, delimiter=',')
        inp, wts, bias, outpR = None, None, None, None
        for row in XY:
            if not inp:
                inp = {}
                for i in range(0, len(inpL)):
                    inp[inpL[i]] = float(row[i])
            elif not wts:
                wts = {}
                cnt = 0
                layers = []
                layers.append(inpL)
                layers.extend(hiddenL)
                layers.append(outpL)
                # pprint.pprint(row)
                for i in range(0, len(layers)-1):
                    for node in layers[i]:
                        for nextN in layers[i+1]:
                            #pprint.pprint(prevN, node, cnt)
                            wts[(node, nextN)] = float(row[cnt])
                            cnt += 1
            elif not bias:
                cnt = 0
                bias = {}
                for hiddenN in hiddenL[0]:
                    bias[hiddenN] = float(row[cnt])
                    cnt += 1
                for outpN in outpL:
                    bias[outpN] = float(row[cnt])
                    cnt += 1
            elif not outpR:
                outpR = {}
                for i in range(0, len(outpL)):
                    outpR[outpL[i]] = float(row[i])
        return inp, wts, bias, outpR


l = float(input("Learning Rate:"))
iter = int(input("Iterations: "))
print('\nInput Taken')
inpL, hiddenL, outpL = get_nn()
inp, wts, bias, outpR = get_desc(inpL, hiddenL, outpL)
layers = []
layers.append(inpL)
layers.extend(hiddenL)
layers.append(outpL)
pprint.pprint(inpL)
pprint.pprint(hiddenL)
pprint.pprint(outpL)
pprint.pprint(inp)
pprint.pprint(wts)
pprint.pprint(bias)
pprint.pprint(outpR)
pprint.pprint(layers)

while iter > 0:
    print("\nIter Remaining", iter, "\n")
    outp = {}
    for i in range(0, len(layers)):
        if i == 0:
            for node in layers[0]:
                outp[node] = inp[node]
            continue
        for node in layers[i]:
            summation = 0
            # pprint.pprint(node)
            for prevN in layers[i-1]:
                # pprint.pprint(wts[(prevN, node)], outp[prevN])
                summation += wts[(prevN, node)]*outp[prevN]
            summation += bias[node]
            outp[node] = 1/(1+math.exp(-summation))
    print()
    pprint.pprint("Output")
    pprint.pprint(outp)

    # Calculating error
    err = {}
    for i in reversed(range(0, len(layers))):
        if i == len(layers)-1:
            for node in layers[i]:
                err[node] = outp[node]*(1-outp[node])*(outpR[node]-outp[node])
        elif i == 0:
            continue
        else:
            for node in layers[i]:
                summation = 0
                for nextN in layers[i+1]:
                    summation += wts[(node, nextN)]*err[nextN]
                err[node] = outp[node]*(1-outp[node])*summation
    print()
    pprint.pprint("Error")
    pprint.pprint(err)

    # Calculating weights
    delw = {}
    for nodes, wt in wts.items():
        i, j = nodes
        delw[nodes] = l*err[j]*outp[i]
        wts[nodes] += delw[nodes]
    print()
    pprint.pprint("Delta Wts")
    pprint.pprint(delw)
    print()
    pprint.pprint("New Wts")
    pprint.pprint(wts)

    # Calculating biases
    delb = {}
    for node, b in bias.items():
        delb[node] = l*err[node]
        bias[node] += delb[node]
    print()
    pprint.pprint("Delta Biases")
    pprint.pprint(delb)
    print()
    pprint.pprint("New Biases")
    pprint.pprint(bias)
    iter -= 1
