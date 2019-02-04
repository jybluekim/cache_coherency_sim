import unittest
from msi import *
import random


class msi_test(unittest.TestCase):
    def test_random(self):


        p_lst = []
        p_count = 3

        bus = Bus()
        
        for i in range(p_count):
            st = "p" + str(i)
            p = Processor(st)
            p_lst.append(p)
            bus.add_processor(p)
            p.add_bus(bus)
         

        test_len = 20
        addr_range = 10

        # randomness
        # 1. which processor
        # 2. commands: PrRd, PrWr
        # 3. In case of write, write value
        # 4. Address - we can start with fixed address

        
        for i in range(test_len):
            p = random.randint(0, p_count - 1)
            RW = random.randint(1, 10) # say 70% read, 30% write
            val = random.randint(1,100)
            addr = random.randint(0, addr_range - 1)
            if RW <= 7:
                p_lst[p].PrRd(addr)
                print ("Instruction number: ", i, ", PrRd for processor number ", p)
            else:
                p_lst[p].PrWr(addr, val)
                print ("Instruction number: ", i, ", PrWr for processor number ", p, ", value: ", val)
            
            self.dump(p_lst, bus)




    def dump(self, p_lst, bus):
        for p in p_lst:
            p.dump()
        print (bus.mem)

if __name__ == "__main__":
    unittest.main(verbosity=2)