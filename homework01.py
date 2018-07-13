i=0
s=0
while True:
    a=raw_input("Enter Value: ")
    if a=='':                         #press 'enter key' loop end
        break
    elif a.isdigit()==True:           #check value'a' is type int
        i=int(a)
        s=s+i
print('Sum of the Your Values: %d' %s)
