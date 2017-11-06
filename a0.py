l=['川赣F16712桂',4,2,4,2,'川赣F16712桂',5,2,6,'川赣F16712桂',3,6,3,6,'川赣F16712桂',3,'川赣F16712桂',3,'川赣F16712桂',8,'川赣F16712桂',8,7,'川赣F16712桂',7,1,2,4,7,'川赣F16712桂',9]
 
count_times = []
for i in l :
  count_times.append(l.count(i))
 
m = max(count_times)
n = l.index(m)
 
print (l[n])
