
# coding: utf-8

# In[ ]:


import asyncio

data_to_save = {}


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
    
    def data_received(self, data):
        data = data.decode()
        data = data.split(' ')
    
        if data[0]=='put' and len(data)==4 and data[3][-1]=='\n' and isinstance(data[1], str) and isinstance(float(data[2]), float) and isinstance(data[3], str):
            if (data_to_save.get(data[1]) is not None) and ((data[2], data[3]) in data_to_save.get(data[1])):
                pass
            else:
                data_to_save.setdefault(data[1], []).append((data[2], data[3]))
        
            self.transport.write(b'ok\n\n')
        
        elif data[0]=='get' and data[1]!='*\n' and data[1][-1]=='\n' and isinstance(data[1], str):
            my_key = data[1][:-1]
            data_to_send = ''
            if data_to_save.get(my_key) is not None:
                for data in data_to_save.get(my_key):
                    my_str = str(my_key) + ' ' + str(data[0]) + ' ' + str(data[1])
                    data_to_send = data_to_send + my_str
                str_to_send = 'ok\n' + data_to_send + '\n\n'
                self.transport.write(bytes(str_to_send, 'utf-8'))
            else:
                self.transport.write(bytes('ok\n\n', 'utf-8'))
        
        elif data[0]=='get' and data[1]=="*\n":
            data_to_send = ''
            if len(data_to_save.items())>0:
                for key in data_to_save.keys():
                    for data in data_to_save.get(key): 
                        my_str = str(key) + ' ' + str(data[0]) + ' ' + str(data[1])
                        data_to_send = data_to_send + my_str
                str_to_send = 'ok\n' + data_to_send + '\n\n'
                self.transport.write(bytes(str_to_send, 'utf=8'))
            else:
                self.transport.write(bytes('ok\n\n', 'utf-8'))
            
        
        else:
            err_str = 'error\nwrong command\n\n'
            self.transport.write(bytes(err_str, 'utf=8'))
    
def run_server(host, port):
    
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    
    server = loop.run_until_complete(coro)
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    
#if __name__ == "__main__":
#    run_server("127.0.0.1", 8181)

