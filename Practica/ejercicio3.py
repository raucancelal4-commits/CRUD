matematicas={"Ana", "Luis", "Sol", "Marco"}
ingles={"Luis","Marco","Ruth"}
ambas       = matematicas & ingles     
solo_mate   = matematicas - ingles     
total       = len(matematicas | ingles)  
print(sorted(ambas))
print(sorted(solo_mate)) 
print(total)