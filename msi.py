''' 
Goal: write a SMP with MSI coherence scheme
    M: modified
    S: shared
    I: invalidated



Classes 

* Processor

* Interconnect 

'''


class Bus:
    def __init__(self):
        self.p_lst = []
        self.mem_size = 10
        self.mem = [ 100+i for i in range(self.mem_size)] 
    def add_processor(self, p):
        self.p_lst.append(p)

    def BusRd(self, p, addr):
        for i in self.p_lst:
            if i != p:
                i.BusRd(addr)
            
        return self.mem[addr]

    def BusRdX(self, p, addr):
        for i in self.p_lst:
            if i != p:
                i.BusRdX(addr)
            
        return self.mem[addr]

    def BusWr(self, addr, val ):
        self.mem[addr] = val

class Processor:

    def __init__(self, name):
        self.name = name
        self.bus = None
        self.cache_size = 10
        self.cache = [ {"status": "I", "data": 0} for i in range(self.cache_size) ]

    def add_bus(self, b):
        self.bus = b

    # in case of a flush, you write the (local) data in the address to the bus
    def flush(self, addr):
        self.bus.BusWr(addr, self.cache[addr]["data"])


    def dump(self):
        print ("Dump for ", self.name)
        for i in range(self.cache_size):
            print (i, self.cache[i]["status"], self.cache[i]["data"])


    ######
    ## there are 4 possible inputs to the processor cache
    ## So in each case we will react to the pre-set rules and may generate output and transition to different state
    #######

    def PrRd(self, addr):
        if self.cache[addr]["status"] == "I":
            ret = self.bus.BusRd(self, addr)
            self.cache[addr]["status"] = "S"
            self.cache[addr]["data"] = ret
            return ret
        elif self.cache[addr]["status"] == "M":
            return self.cache[addr]["data"]             
        elif self.cache[addr]["status"] == "S":
            ret = self.bus.BusRd(self, addr)
            self.cache[addr]["status"] = "S"
            self.cache[addr]["data"] = ret
            return ret

    # this is when you get BusRd as input (i.e. other processor is issuing BusRd and the Bus is broadcasting it)
    def BusRd(self, addr):
        if self.cache[addr]["status"] == "I":
            pass
        elif self.cache[addr]["status"] == "M":
            self.flush(addr)
            self.cache[addr]["status"] = "S"
        elif self.cache[addr]["status"] == "S":
            pass


    def PrWr(self, addr, val):
        if self.cache[addr]["status"] == "I":
            ret = self.bus.BusRdX(self, addr)
            self.cache[addr]["data"] = val
            self.cache[addr]["status"] = "M"

        elif self.cache[addr]["status"] == "M":
            self.cache[addr]["data"] = val
        elif self.cache[addr]["status"] == "S":
            ret = self.bus.BusRdX(self, addr)
            self.cache[addr]["data"] = val
            self.cache[addr]["status"] = "M"
            

    def BusRdX(self, addr):
        if self.cache[addr]["status"] == "I":
            pass
        elif self.cache[addr]["status"] == "M":
            self.flush(addr)
            self.cache[addr]["status"] = "I"
        elif self.cache[addr]["status"] == "S":
            self.cache[addr]["status"] = "I"

''' 

State diagram of MSI

Inputs: 
    From processor: PrRd, PrWr
    From bus: BusRd, BusRdX, 

Outputs: 
    BusRdX, BusRd, Flush

curr, input, output, next
I, PrRd, BusRd, S
I, PrWr, BusRdX, M
I, BusRd, -, I
I, BusRdX, -, I
M, PrRd, -, M
M, PrWr, -, M
M, BusRd, Flush, S
M, BusRdX, Flush, I
S, PrRd, BusRd, S
S, PrWr, BusRdX, M
S, BusRdX, -, I
S, BusRd, -, S




'''



'''

Possible scenario

1. P1 PrRd - BusRd, data comes in and becomes S
2. P2 PrRd - BusRd, data comes in and also becomes S
3. P3 PrWr - BusRdX (exclusive), invalidates P1 and P2, data comes to P3 but becomes M
4. P2 PrRd - flush P3's value, and both P2 and P3 data becomes S
5. P1 wants to write - bus readX, invalidates P2 and P3, data comes to P1 and becomes M
6. P2 wants to write - flush P1's value, P2 gets M and P1 and P3 gets I


'''


def dump(p_lst, bus):
    for p in p_lst:
        p.dump()
    print (bus.mem)

if __name__ == "__main__":
    
    
    
    p1 = Processor("p1")
    p2 = Processor("p2")
    p3 = Processor("p3")
    bus = Bus()
    bus.add_processor(p1)
    bus.add_processor(p2)
    bus.add_processor(p3)
    p1.add_bus(bus)
    p2.add_bus(bus)
    p3.add_bus(bus)


    # start from I, this moves p1.7 to M
    p1.PrWr(7, 17)
    print ("p1.PrWr(7, 17)")
    dump([p1, p2, p3], bus)

    # Reading it from p1 does not change status
    p1.PrRd(7)
    print ("p1.PrRd(7)")
    dump([p1, p2, p3], bus)

    # You can even write new value and it will only affect p1 cache and have no other affect
    p1.PrWr(7, 18)
    print ("p1.PrWr(7, 18)")
    dump([p1, p2, p3], bus)


    # If P2 is doing PrWr to the same location,  
    # this generates global BusRdX
    # and it will invalidate p1.7
    p2.PrWr(7, 27)
    print ("p2.PrWr(7, 27)")
    dump([p1, p2, p3], bus)

    # Start from I, now we do PrRd and this should put P1.7 in S state
    p1.PrRd(7)
    print ("p1.PrRd(7)")
    dump([p1, p2, p3], bus)

    # 
    p3.PrRd(7)
    print ("p3.PrRd(7)")
    dump([p1, p2, p3], bus)



'''
    p1.PrRd(7)
    dump([p1, p2, p3], bus)

    p2.PrRd(7)
    dump([p1, p2, p3], bus)

    p3.PrWr(7, 37)
    dump([p1, p2, p3], bus)

    p2.PrRd(7)
    dump([p1, p2, p3], bus)

    p1.PrWr(7, 17)
    dump([p1, p2, p3], bus)
    
    p2.PrWr(7, 27)
    dump([p1, p2, p3], bus)


    '''