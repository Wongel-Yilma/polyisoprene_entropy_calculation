import numpy as np

f = open("polyisoprene.lt",'a')

f.write("import \"repeat.lt\"\n")
f.write("import \"head.lt\"\n")
f.write("import \"tail.lt\"\n")
f.write("Polyisoprene inherits OPLSAA {\n")
f.write("  create_var {$mol}\n")
f.write("monomers[0] = new HEAD.move(0.0,0,0)\n")
for i in range(1,149):
    f.write(f"monomers[{i}] = new C5H8.move({7*i},0.0,0)\n")

f.write(f"monomers[{i+1}] = new TAIL.move({7*(i+1)},0.0,0)\n")
f.write("write('Data Bond List') {\n")

for k in range(149):
    f.write(f"$bond:b{k+1}  $atom:monomers[{k}]/c5 $atom:monomers[{k+1}]/c4\n")
f.write("\n")
f.write('}\n')

f.write('}\n')
