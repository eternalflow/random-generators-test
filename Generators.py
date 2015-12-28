from random import getrandbits, randint

class Generator(object):

    def __init__(self):
        pass

    def next(self):
    	return 0
        pass

    def get_byte(self):
    	byte = 0
    	for i in xrange(8):
    		byte <<= 1
    		byte += self.next()

    	return byte

    def gen_bytes(self, n):
   		counter = 0
   		while counter < n:
   			yield self.get_byte()
   			counter += 1


class PythonRandom(Generator):

    def __init__(self):
    	super(PythonRandom, self).__init__()
        pass

    def next(self):
        return getrandbits(1)
        pass


class Lehmer(Generator):

    def __init__(self, c, a, m):
    	#c, a, m = 119, 2**16 + 1, 2**32
        self.c = c
        self.a = a
        self.m = m
        self.x0 = randint(1, m)
        self.prev = self.x0
        pass

    def get_number(self):
        self.prev = (self.a*self.prev + self.c) % self.m
        return self.prev
        pass
    pass

class LehmerHigh(Lehmer):
    
    def get_byte(self):
        big = self.get_number()
        byte = big >> 24
        return byte

    pass


class LehmerLow(Lehmer):

    def get_byte(self):
        big = self.get_number()
        return big & 0b11111111
        pass

    pass

class Linear(Generator):

    def __init__(self, state, polynome):
        self.state = state
        self.polynome = polynome
        pass

    def next(self):
        result = 0
        for index in self.polynome:
            result = (result + self.state[index]) & 1

        first, self.state = self.state[0], self.state[1:] + [result]
        return first
        pass

    pass

class Geffe(Generator):

    def __init__(self, L1, L2, L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        pass

    def next(self):
        x = self.L1.next()
        y = self.L2.next()
        s = self.L3.next()
        return (s*x + ((1 + s) & 1)*y) & 1
        pass

    pass

class Libraryman(Generator): 

	def __init__(self, filename): 
		self.text = [] 
		with open(filename) as file: 
			for line in file: 
				self.text.append(line) 
				pass 
			pass 
		self.line = randint(0, len(self.text)-1) 
		self.pos = 0 
		pass 

	def get_byte(self): 
		if self.pos >= len(self.text[self.line]): 
			self.line = randint(0, len(self.text)-1) 
			self.pos = 0 
			pass 

		byte = ord(self.text[self.line][self.pos]) 
		self.pos += 1 
		return byte 
		pass 

	pass 

def pow_mod(x, power, modulo):
	bin_array = (power>>i & 1 for i in reversed(xrange(power.bit_length())))
	result = 1
	for exp in bin_array:
		result = (result * result % modulo) * (x**exp) % modulo
	return result

class BM(Generator):

	def __init__(self, p, a):
		self.p = p
		self.a = a
		self.t = randint(0, p-1)
		self.conditional_p = (self.p - 1)/2
		pass

	def next(self):
		x = 1
		if self.t >= self.conditional_p:
			x = 0
			pass

		self.t = pow_mod(self.a, self.t, self.p)
		return x
		pass

	pass

	
class BM_bytes(Generator):

	def __init__(self, p, a):
		self.p = p
		self.a = a
		self.t = randint(0, p-1)
		self.conditional_p = (self.p - 1)/256
		pass

	def get_byte(self):
		for k in range(256):
			if k*self.conditional_p < self.t <= (k+1)*self.conditional_p:
				self.t = pow_mod(self.a, self.t, self.p)
				return k
				pass		
			pass
		pass
	pass

class BBS(Generator):

	def __init__(self, p, q):
		self.p = p
		self.q = q
		self.n = p*q
		self.r = randint(2, self.n)
		pass

	def next(self):
		self.r = (self.r*self.r) % self.n
		return self.r & 1
		pass
	pass

class BBS_bytes(Generator):

	def __init__(self, p, q):
		self.p = p
		self.q = q
		self.n = p*q
		self.r = randint(2, self.n)
		pass

	def get_byte(self):
		self.r = (self.r*self.r) % self.n
		return self.r % 256
		pass

	pass