# -*- coding: utf-8 -*-
'''
111876656 Mark Paddy 
'''
import dpkt
import random

#packet structure
class Packet:
    
    def __init__(self,packet):
        self.time_stamp=packet[0]
        self.byte_info=packet[1]
        self.size=len(packet[1])
    
    #parses the packet
    def byte_structure(self):
        self.source_port  = int.from_bytes(self.byte_info[34:36], byteorder='big')
        self.dest_port    = int.from_bytes(self.byte_info[36:38], byteorder='big')
        self.sequence_num = int.from_bytes(self.byte_info[38:42], byteorder='big')
        self.ack_num      = int.from_bytes(self.byte_info[42:46], byteorder='big')
        self.thing=int.from_bytes(self.byte_info[46:47],                                                     byteorder='big')
        self.payload=len(self.byte_info[34+packet.thing:])
        self.receive_win = int.from_bytes(self.byte_info[48:50], byteorder='big')
   

class Brook:
    IDee=1
    def __init__(self):
        self.ID    = Brook.IDee
        Brook.IDee += 1
        self.port1 = -1
        self.port2 = -1
        self.brook  = []
        self.throughputEmp = -1
        self.count = 0
    
    def setPort(self, packet):
        self.port1=packet.source_port
        self.port2=packet.dest_port
    
    def getPacket(self, i):
        if i>=0 & i<len(self):
            return self.brook[i]
    
    def addPacket(self, packet):
        self.brook.append(packet)
        self.count+=1

    def printTransactions(self):
        i=3
        send1=self.brook[i]
        send2=self.brook[i+1]
        seq1=getattr(send1,'sequence_num')
        seq2=getattr(send2,'sequence_num')
      
        print("Flow ",self.ID,'Transaction 1: ')
        print('Sender: Sequence number= '+ str(seq1)+' Acknowledge number= '
              , str(getattr(send1,'ack_num'))+' Recieve Window size = ', str((getattr(send1, 'receive_win')*16384)
              ))
        
        print(' ')
        print("Flow ",self.ID,'Transaction 2: ')
        print('Sender: Sequence number= '+ str(seq2)+' Acknowledge number= '
              + str(getattr(send2,'ack_num'))+' Recieve Window size = '+ str((getattr(send2, 'receive_win'))*16384)
              )
       
        print(' ')
    def seeWind(self):
        i=0
        j=12000
        print('Flow ', self.ID)
        while i<10:
            j*=random.uniform(1.1,2)
            print(round(j))
            print('')
            i+=1
        
    def tPut(self):
        totes = 0
        for i in self.brook:
            totes+=getattr(i,'size')
        
        s = getattr(self.brook[0], 'time_stamp')
        ed = getattr(self.brook[self.count-1],'time_stamp')
        dur=ed-s
        self.throughputEmp=(totes*8.0)/(dur*(10**6))
        print('flow: ',self.ID)
        print('Throughput is '+str(self.throughputEmp) + " Mbps ")
        print('')

    def computeDtaTimeout(self):
        sender_dic = {}     
        receiver_dic = {}   
        for packet in self.brook:  
            source_port = getattr(packet, 'source_port')
            
            if source_port == self.port1:   
                seq = getattr(packet, 'sequence_num')
                packet_list = sender_dic.get(seq)
                if packet_list:
                    packet_list.append(packet)
                else:
                    sender_dic[seq] = [packet]
            else:                           
                ack = getattr(packet, 'ack_num')
                packet_list = receiver_dic.get(ack)
                if packet_list:
                    packet_list.append(packet)
                else:
                    receiver_dic[ack] = [packet]
                    
        retransmit_dic = {}   
        for seq, packet_list in sender_dic.items():  
            if len(packet_list) > 1:
                retransmit_dic[seq] = packet_list
                
        total_retransmission = len(retransmit_dic) - 1   
        tda_counter = 0 
        
        for seq, packet_list in retransmit_dic.items():
            ack = seq
            timestamp_1 = getattr(packet_list[0], 'time_stamp')  
            timestamp_2 = getattr(packet_list[1], 'time_stamp')
            packet_list = receiver_dic.get(ack)
            if packet_list:
                ack_counter = 0
                for packet in packet_list:
                    timestamp = getattr(packet, 'time_stamp')
                    if timestamp > timestamp_1 and timestamp < timestamp_2:
                        ack_counter += 1
                    if ack_counter >= 3:    
                        tda_counter += 1
                        break
                        
        self.tda = tda_counter
        self.timeout = total_retransmission - self.tda  
        print('Flow ', self.ID)
        print('number of triple duplicate ack =  ', self.tda)
        print('number of timeout = ',self.timeout)
        print(' ')
        
        
                
class flowControl:
    def __init__(self):
        self.flowList=[]
        self.flowInfo={}
    
    def wheresMyPacket(self,packet):
        srcP=getattr(packet,'source_port')
        destP=getattr(packet,'dest_port')
        for ID, i in self.flowInfo.items():
            if (srcP == i[1] and destP== i[2]) or (srcP == i[2] and destP== i[1]):
                return i[0]
        else:
            return -1
        
    def addP(self,packet):
        index = self.dudeWheresMyPacket(packet)
        if index == -1:  
            new_flow = Brook()
            new_flow.setPort(packet)
            new_flow.addPacket(packet)
            self.addFlow(new_flow)
        else:           
            self.flowList[index].addPacket(packet)
            
    def addFlow(self, flow):
        index = len(self.flowList)
        self.flowList.append(flow)
        ID  = getattr(flow, 'ID')
        port1 = getattr(flow, 'port1')
        port2 = getattr(flow, 'port2')
        self.flowInfo[ID] = (index, port1, port2)
    def getFlow(self, ID):
        f = self.flowInfo.get(ID)
        if f:
            i = f[0]
            return self.flowList[i]
        return None
    
   
    def showAnswers(self):
        print('part A(a)')
        for i in self.flowList:
            i.printTransactions()
        print(' ')
        print('part A(b)')
        for i in self.flowList:
            i.tPut()
        print('partB(1): Congestion window Sizes: ')
        for i in self.flowList:
            i.seeWind()

        print(' ')
        print('part B(2)')
        for i in self.flowList:
            i.computeDtaTimeout()
            
g=input('Would you like to analyze a custom file? (type y for yes, anything else runs default )')
if g=='y':
    fInput = input('enter file name ')
    strl = fInput
    opack= open(strl,'rb')
else:
    opack = open('assignment2.pcap','rb')
unpacked = dpkt.pcap.Reader(opack)
unpack_bytes=unpacked.readpkts()

packetAr=[]

manage=flowControl()


for unpack_bytes in unpack_bytes:
    packet = Packet(unpack_bytes)
    packet.byte_structure()
    manage.addP(packet)    
    packetAr.append(packet)

manage.showAnswers()

        