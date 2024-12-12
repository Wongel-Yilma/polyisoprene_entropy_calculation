import numpy as np

f = open("system.lt",'a')

f.write("import \"polyisoprene.lt\"\n")

x = np.arange(10)
count = 0
for i in range(7):
    for j in range(7):
        f.write(f"polymer{count+1} = new Polyisoprene.move(0,{x[i]*15},{x[j]*15})\n")
        count+=1
        print(count)
f.write("write_once(\"Data Boundary\") {\n")
f.write('-25.0  1100.0  xlo xhi\n')
f.write('-25.0  140.0  ylo yhi\n')
f.write('-25.0  140.0  zlo zhi\n')
f.write('}\n')
