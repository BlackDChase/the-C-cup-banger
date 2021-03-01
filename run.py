from course.DataMining.dm import ID3
import sys

def questionID3():
    # ID3 Decision Tree
    print("""
Example:
    Outlook :   Sunny,Sunny,Overcast,Rain,Rain
    Temp    :   79,56,88,78,66
    Play    :   No Play,Play,No Play,No Play,Play
    Play
    """)
    data={}
    target=None
    while True:
        line = input()
        k,v = None,None
        if ":" in line:
            k,v = line.split(":")
            v = v.split(",")
            v = [i.strip() for i in v]
            data[k.strip()] = v
        else:
            target = line.strip()
            break
    print(target,"\n",data)
    question = ID3(data,target)
    print("System entropy {:.4f}".format(question.entropy))
    question.id3()
    question.printTree()
    pass

def exit():
    print("See you next C")
    sys.exit()

Question = {
    "1":["Make DecisionTree",questionID3],
    "0":["Exit",exit],
}

if __name__=='__main__':
    print("Welcome to the C Banger")
    while True:
        print("**********************")
        for i in Question.keys():
            print(i," For ",Question[i][0])
        q = input("Option: ")
        Question[q][1]()
