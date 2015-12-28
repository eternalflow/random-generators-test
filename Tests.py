from random import randint
from Generators import *
from pickle import dump, load
from csv import DictWriter

def test1(seq, quantile):
	v = [0]*256
	n = 0
	hi_square = 0

	for byte in seq:
		n += 1
		v[byte] += 1

	nj = n/256
	for j in v:
		hi_square += (j - nj)**2.0 / nj

	l = 255
	hi_square_edge = (2*l)**0.5 * quantile + l

	result = {  
				"length": n,
				"hi_square": hi_square,
				"hi_square_edge": hi_square_edge,
				"passed": hi_square <= hi_square_edge
			 }

	return result
	pass

def test2(seq, quantile):

	def gen_pairs(s):
		ind = 0
		while True:
			try:
				byte1 = s[ind]
				byte2 = s[ind+1]
				yield byte1, byte2
			except:
				break
			ind += 2

	pairs = gen_pairs(seq)
	n = 0
	count_pairs = {}
	v, a = [0]*256, [0]*256
	for pair in pairs:
		n += 1
		if pair not in count_pairs:
			count_pairs[pair] = 0
		count_pairs[pair] += 1
		v[pair[0]] += 1
		a[pair[1]] += 1

	hi_square = 0
	for i in xrange(256):
		for j in xrange(256):
			if v[i] != 0 and a[j] != 0:
				if (i, j) not in count_pairs:
					continue
				hi_square += count_pairs[(i, j)] ** 2.0 / (v[i] * a[j])
	hi_square -= 1
	hi_square *= n

	l = 255**2
	hi_square_edge = (2*l)**0.5 * quantile + l

	result = {  
				"length": n*2,
				"hi_square": hi_square,
				"hi_square_edge": hi_square_edge,
				"passed": hi_square <= hi_square_edge
			 }
			 
	return result
	pass


def test3(seq, quantile, r): 
	m = len(seq)
	slice_len = m/r
	n = slice_len * r
	slices_ = [] 
	for i in range(0, n, slice_len): 
		slice_ = seq[i:i+slice_len] 
		slices_.append(slice_) 
		pass 

	def count_bytes(byte, array): 
		count = 0 
		for el in array: 
			if el == byte: 
				count += 1 
		return count 
		pass 

	v = [0]*256
	for byte in seq[:n]:
		v[byte] += 1

	aj = slice_len
	hi_square = 0 
	for byte in range(256): 
		for slice_ in slices_: 
			vij = count_bytes(byte, slice_) 

			if v[byte] != 0:
				hi_square += (vij**2.0) / (v[byte] * aj) 

	hi_square -= 1
	hi_square *= n
	l = 255 * (r-1) 
	hi_square_edge = ( (2*l)**0.5 ) * quantile + l 

	result = {  
				"length": n,
				"slice_length": slice_len,
				"count_slices": r,
				"hi_square": hi_square,
				"hi_square_edge": hi_square_edge,
				"passed": hi_square <= hi_square_edge
			 }
	return result
	pass

# length_test = 125000
# #1
# python = PythonRandom()
# #2,3
# c, a, m = 119, 2**16 + 1, 2**32
# lehmer_low = LehmerLow(c,a,m)
# lehmer_high = LehmerHigh(c,a,m)
# #4
# state20 = [randint(0,1) for i in range(20)]
# L20 = Linear(state20, [0, 11, 15, 17])
# #5
# state89 = [randint(0,1) for i in range(89)]
# L89 = Linear(state89, [0, 51])
# #6
# state11 = [randint(0,1) for i in range(11)]
# state9 = [randint(0,1) for i in range(9)] 
# state10 = [randint(0,1) for i in range(10)]
# L11 = Linear(state11, [0, 2])
# L9 = Linear(state9, [0, 1, 3, 4])
# L10 = Linear(state10, [0, 3])
# geffe = Geffe(L1=L11, L2=L9, L3=L10)
# #7
# libraryman = Libraryman("saved_seqs/kant.txt") 
# #8
# p = 0xcea42b987c44fa642d80ad9f51f10457690def10c83d0bc1bcee12fc3b6093e3
# a = 0x5b88c41246790891c095e2878880342e88c79974303bd0400b090fe38a688356
# bm = BM(p, a)
# #9
# bm_bytes = BM_bytes(p, a)
# #10
# p = 0xd5bbb96d30086ec484eba3d7f9caeb07
# q = 0x425d2b9bfdb25b9cf6c416cc6e37b59c1f
# bbs = BBS(p, q)
# #11
# bbs_bytes = BBS_bytes(p, q)


# std_python_seq = python.gen_bytes(length_test)
# lehmer_low_seq = lehmer_low.gen_bytes(length_test)
# lehmer_high_seq = lehmer_high.gen_bytes(length_test)
# L20_seq = L20.gen_bytes(length_test)
# L89_seq = L89.gen_bytes(length_test)
# geffe_seq = geffe.gen_bytes(length_test)
# lib_seq = libraryman.gen_bytes(length_test)
# bm_seq = bm.gen_bytes(length_test)
# bm_bytes_seq = bm_bytes.gen_bytes(length_test)
# bbs_seq = bbs.gen_bytes(length_test)
# bbs_bytes_seq = bbs_bytes.gen_bytes(length_test)



with open("saved_seqs/std_python_seq.seq", "rb") as f:
	std_python_seq = load(f)
with open("saved_seqs/lehmer_low_seq.seq", "rb") as f:
	lehmer_low_seq = load(f)
with open("saved_seqs/lehmer_high_seq.seq", "rb") as f:
	lehmer_high_seq = load(f)
with open("saved_seqs/L20_seq.seq", "rb") as f:
	L20_seq = load(f)
with open("saved_seqs/L89_seq.seq", "rb") as f:
	L89_seq = load(f)
with open("saved_seqs/geffe_seq.seq", "rb") as f:
	geffe_seq = load(f)
with open("saved_seqs/lib_seq.seq", "rb") as f:
	lib_seq = load(f)

with open("saved_seqs/bm_seq.seq", "rb") as f:
	bm_seq = load(f)

with open("saved_seqs/bm_bytes_seq.seq", "rb") as f:
	bm_bytes_seq = load(f)
with open("saved_seqs/bbs_seq.seq", "rb") as f:
	bbs_seq = load(f)
with open("saved_seqs/bbs_bytes_seq.seq", "rb") as f:
	bbs_bytes_seq = load(f)

sequences = (
			  ("std_python", std_python_seq),
			  ("lehmer_low", lehmer_low_seq),
			  ("lehmer_high", lehmer_high_seq),
			  ("L_20", L20_seq),
			  ("L_89", L89_seq),
			  ("Geffe", geffe_seq),
			  ("Libraryman", lib_seq),
			  ("BM", bm_seq),
			  ("BM_bytes", bm_bytes_seq),
			  ("BBS", bbs_seq),
			  ("BBS_bytes", bbs_bytes_seq)
			)

print "Test 1"

with open("test1.csv", "w") as f:
	fieldnames = ["name", "length", "hi_square", "hi_square_edge", "passed"]
	writer = DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()

	for name, seq in sequences:
		result = test1(seq, 2.4)
		print name, "done"
		result["name"] = name
		writer.writerow(result)
		pass
	pass

print "Test 2"

with open("test2.csv", "w") as f:
	fieldnames = ["name", "length", "hi_square", "hi_square_edge", "passed"]
	writer = DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()

	for name, seq in sequences:
		result = test2(seq, 2.4)
		print name, "done"
		result["name"] = name
		writer.writerow(result)
		pass
	pass

print "Test 3"

with open("test3.csv", "w") as f:
	fieldnames = ["name", "length", "slice_length", "count_slices", "hi_square", "hi_square_edge", "passed"]
	writer = DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()

	for name, seq in sequences:
		for count_slices in range(5, 20):
			result = test3(seq, 2.4, count_slices)
			print name, "done, count slices", count_slices
			result["name"] = name
			writer.writerow(result)
			pass
		pass
	pass

	

