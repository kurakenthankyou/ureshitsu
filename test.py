d = { 'grape': 20, 'orange': 30, 'pineapple': 20}
d['apple'] = d.get('apple', -1)
d['pineapple'] = d.get('pineapple')
print(d)

i="training"
print(i[1:5])

l="understand"
print(l[1::2])

p=[1,2,3,4,5]
print(p[::3])

o=[1,1,1,2,3,3,4,4,5,]
print(set(o))

set1={1,2,3,4,5}
set2={3,4,5,6,7}
print(set1&set2)