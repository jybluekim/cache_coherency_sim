import unittest
from msi import *
import random


class msi_test(unittest.TestCase):
    def test_random(self, test_len = 20, addr_range = 10, p_count = 3):


        p_lst = []

        bus = Bus()
        
        for i in range(p_count):
            st = "p" + str(i)
            p = Processor(st)
            p_lst.append(p)
            bus.add_processor(p)
            p.add_bus(bus)
         
 
        # randomness
        # 1. which processor
        # 2. commands: PrRd, PrWr
        # 3. In case of write, write value
        # 4. Address - we can start with fixed address

        
        for i in range(test_len):
            print ("#### Starting new instruction")
            p = random.randint(0, p_count - 1)
            RW = random.randint(1, 10) # say 70% read, 30% write
            val = random.randint(1000,2000)
            addr = random.randint(0, addr_range - 1)
            if RW <= 5:
                p_lst[p].PrRd(addr)
                print ("Instruction number: ", i, ", PrRd for processor number ", p, ", addr: ", addr)
            else:
                p_lst[p].PrWr(addr, val)
                print ("Instruction number: ", i, ", PrWr for processor number ", p, ", addr: ", addr, ", value: ", val)
            
            self.dump(p_lst, bus)




    def dump(self, p_lst, bus):
        for p in p_lst:
            p.dump()
        print ("Main memory: ", bus.mem, "\n")

if __name__ == "__main__":
    unittest.main(verbosity=2)