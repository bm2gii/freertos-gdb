import gdb
from .common import StructProperty, FreeRtosList, print_table
from .task import TaskProperty

class MEMProperty(StructProperty):
    ADDR = ('Slot address', '', 'get_val')
    SIZE = ('Size of slot', '', 'get_val')
    NEXT = ('Next Slot addr', '', 'get_val')


class FreeList:
    def __init__(self, ):
        self._list = []
        self._list_type = gdb.lookup_type("BlockLink_t")

    def print_help(self):
        for _, item in enumerate(MEMProperty):
            item.print_property_help(self._list_type)
        print('')

    def get_table_headers(tcb_type):
        row = []
        #print(tcb_type)
        for _, item in enumerate(MEMProperty):
            #if not item.exist(tcb_type):
            #    continue
            row.append(item.title)
        #print(row)
        return row

    def add_list(self, addr) -> str:
        cmd = "*(BlockLink_t*)%s" %(addr)
        #print(cmd)
        n = gdb.parse_and_eval(cmd)
        #print(n)
        next_item = str(n['pxNextFreeBlock']).split(" ")[0]
        size = str(n['xBlockSize'])
        #print(next_item)
        #print(size)
   
        self._list.append((addr, size, next_item))
        return next_item

    def show(self):
        #print("show 123\n")
        #print(self._list);
        table = []
        for idx, _ in enumerate(self._list):
            table.extend(self.get_table_rows(idx))
        if len(table) == 0:
            return
        self.print_help()
        #print(table)
        print_table(table, self.get_table_headers())

    def get_table_rows(self, q_id):
        table = []
        row = []
        addr, size, next_item = self._list[q_id]
        #print("%d::%s:%s:%s\n" %(q_id, addr, size, next_item)) 


        for _, item in enumerate(MEMProperty):
            val = q_id
            if item is MEMProperty.ADDR:
                val = addr

            if item is MEMProperty.SIZE:
                val = size

            if item is MEMProperty.NEXT:
                val = next_item
                

            #row.append(item.value_str(val))
            row.append(val)
        table.append(row)
        return table

def show_free_list():

    next_item = gdb.parse_and_eval('&xStart')
    #print(next_item)
        
    memlist = FreeList()
    next_item = str(next_item).split(" ")[0]
    #next_item = str(xStart['pxNextFreeBlock']).split(" ")[0]
    #print(next_item)
    
    while(next_item != "0x0"):
        next_item = memlist.add_list(next_item)

    memlist.show()


class FreeRtosFreeMem(gdb.Command):
    """ Dump free memory list.
    """

    def __init__(self):
        super().__init__('freertos mem', gdb.COMMAND_USER)

    @staticmethod
    def invoke(_, __):
        show_free_list()