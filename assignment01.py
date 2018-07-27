import sys
import os.path

def xxd(file_path):
    f=open(file_path,'r')
    s=0
    while True:
        r=f.read(16)
        d=r
        if not r:
            break
        he=[]
        for i in r:
            he.append('%02x'%ord(i))
        he2=[]
        for z in range(0,len(he),2):
            he2.append(''.join((he[z:z+2])))
        ch=[]
        for c in d:
            cc=ord(c)
            if cc<32:
                ch.append('.')
            else:
                ch.append(c)
        step=('%07x'%(s*16))
        print('{0}: {1:<39} {2}'.format(step,' '.join(he2),''.join(ch)))
        s=s+1

if __name__=='__main__':
    if not os.path.exists(sys.argv[1]):
        print('your enter is wrong')
        sys.exit(1)
    xxd(sys.argv[1])
