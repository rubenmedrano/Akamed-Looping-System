from __future__ import with_statement #compatibility for Live 9, need to be written at the first line of the script
import Live #you import Live, in order to be able to use its components
from _Framework.ControlSurface import ControlSurface # import the Controle surface module
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import *
from _Framework.SessionComponent import SessionComponent     #this is the component used to create Sessions
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.TrackArmState import TrackArmState
import time
import threading
from Vars import *


IS_MOMENTARY=True
MASTER={}

DEFINICION={'track':0, 'clip_slot':1}


class AkaMed(ControlSurface):          # create a class element
    __module__=__name__                  #name of the class
    __doc__="AkaMed Looping System for Ableton Live"           #documentation

    def __init__(self, c_instance):           #initialize the AkaMed class as a ControleSurface
        ControlSurface.__init__(self,c_instance)   #import the components of a ControlSurface
        self.__c_instance = c_instance #Puesto por mi para poder usar show_message

        with self.component_guard():               #don't know the us of this, but it is recquiered in live 9 scripts
            #self.show_message('Script initiated')
            self.mensaje("Loading AkaMed for Ableton Live")
            #self.imprime('INICIADO SCAN')
            self.scan()
            #self.imprime('FINALIZADO SCAN')
            #self.press = int(round(time.time() * 1000))
            #self.release = int(round(time.time() * 1000))
            self.long_press = 5.0

            #Create MIDI mapping for FLASH
            for n in range(MASTER['loopers']):
                looper=n+1
                conv1='ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, ' + str(MIDI_CHANNEL-1) + ', FLASH_' + str(looper) + ').add_value_listener(self.boton_flash_' + str(looper) + ', identify_sender= False)'
                exec(str(conv1))

            #Create MIDI mapping for BANKS
            for m in range(MASTER['banks']):
                bank=m+1
                conv1='ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, ' + str(MIDI_CHANNEL-1) + ', BANK_' + str(bank) + ').add_value_listener(self.boton_bank_' + str(bank) + ', identify_sender= False)'
                exec(str(conv1))

            #Create MIDI mapping for UNDO
            for p in range(MASTER['loopers']):
                looper=p+1
                conv1='ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, ' + str(MIDI_CHANNEL-1) + ', UNDO_' + str(looper) + ').add_value_listener(self.boton_undo_' + str(looper) + ', identify_sender= False)'
                exec(str(conv1))

            #Create MIDI mapping for STOP
            for p in range(MASTER['loopers']):
                looper=p+1
                conv1='ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, ' + str(MIDI_CHANNEL-1) + ', STOP_' + str(looper) + ').add_value_listener(self.boton_stop_' + str(looper) + ', identify_sender= False)'
                exec(str(conv1))

            #Create MIDI mapping for AUTO OVERDUB looper
            for p in range(MASTER['loopers']):
                looper=p+1
                conv1='ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, ' + str(MIDI_CHANNEL-1) + ', AUTO_OVERDUB_' + str(looper) + ').add_value_listener(self.boton_auto_overdub_' + str(looper) + ', identify_sender= False)'
                exec(str(conv1))

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, RESET).add_value_listener(self.boton_reset,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, AUTO_OVERDUB).add_value_listener(self.boton_auto_overdub_current,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, PRUEBA).add_value_listener(self.boton_prueba,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, STOP_ALL).add_value_listener(self.boton_all_loopers_stop,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, PLAY_ALL).add_value_listener(self.boton_all_loopers_play,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, UNDO_CURRENT_LOOPER).add_value_listener(self.boton_undo_current,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, COPY).add_value_listener(self.boton_copy,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, CUT).add_value_listener(self.boton_cut,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, PASTE).add_value_listener(self.boton_paste,identify_sender= False)

            ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, MIDI_CHANNEL-1, BANK_FLASH).add_value_listener(self.boton_bank_flash,identify_sender= False)

            #initialisation of the session
            #self.create_session_control()
            #self.set_highlighting_session_component(self.Session)        #link the session model to the Live object-> shows your ring


    def disconnect(self):              #this function is automatically called by live when the program is closed
        pass

    def mensaje(self, mensaje):
        self.__c_instance.show_message(mensaje)

    def boton_prueba(self, value):
        if value!=0:
            self.get_current_layer(1,1)

    def boton_reset(self, value):
        if value!=0:
            self.scan()


    def boton_all_loopers_stop(self, value):
        if value!=0:
            self.all_loopers_stop()

    def boton_copy(self, value):
        if value!=0:
            self.copy_in()
            pass

    def boton_cut(self, value):
        if value!=0:
            #self.cut()
            pass

    def boton_paste(self, value):
        if value!=0:
            #self.paste()
            pass

    def boton_all_loopers_play(self, value):
        if value!=0:
            self.all_loopers_play(MASTER['current_bank'])

    #Bank buttons

    def boton_bank_1(self, value):
        if value!=0:
            self.select_bank(1)
            #self.all_loopers_stop()
            self.change_to_bank(1)
            #Move the red box
            #s=self.detecta_numero_escenas_por_banco() #Gets the number of scenes per bank
            #for n in range(s):
                #self.Session._bank_up()

    def boton_bank_2(self, value):
        if value!=0:
            self.select_bank(2)
            #self.all_loopers_stop()
            self.change_to_bank(2)


    def boton_bank_3(self, value):
        if value!=0:
            self.select_bank(3)
            #self.all_loopers_stop()
            self.change_to_bank(3)


    def boton_bank_4(self, value):
        if value!=0:
            self.select_bank(4)
            #self.all_loopers_stop()
            self.change_to_bank(4)


    def boton_bank_5(self, value):
        if value!=0:
            self.select_bank(5)
            #self.all_loopers_stop()
            self.change_to_bank(5)


    def boton_bank_6(self, value):
        if value!=0:
            self.select_bank(6)
            #self.all_loopers_stop()
            self.change_to_bank(6)


    def boton_bank_7(self, value):
        if value!=0:
            self.select_bank(7)
            #self.all_loopers_stop()
            self.change_to_bank(7)


    def boton_bank_8(self, value):
        if value!=0:
            self.select_bank(8)
            #self.all_loopers_stop()
            self.change_to_bank(8)


    def boton_bank_9(self, value):
        if value!=0:
            self.select_bank(9)
            #self.all_loopers_stop()
            self.change_to_bank(9)


    def boton_bank_10(self, value):
        if value!=0:
            self.select_bank(10)
            #self.all_loopers_stop()
            self.change_to_bank(10)


    def boton_bank_11(self, value):
        if value!=0:
            self.select_bank(11)
            #self.all_loopers_stop()
            self.change_to_bank(11)


    def boton_bank_12(self, value):
        if value!=0:
            self.select_bank(12)
            #self.all_loopers_stop()
            self.change_to_bank(12)

    def boton_bank_flash(self, value):
        if value!=0:
            if MASTER['current_bank']==MASTER['banks']:
                MASTER['current_bank']=1
                self.change_to_bank(1)
            else:
                MASTER['current_bank']+=1
                self.change_to_bank(MASTER['current_bank'])

    #Flash buttons

    def boton_flash_1(self, value):
        if value!=0:
            self.looper_run(1)

    def boton_flash_2(self, value):
        if value!=0:
            self.looper_run(2)

    def boton_flash_3(self, value):
        if value!=0:
            self.looper_run(3)

    def boton_flash_4(self, value):
        if value!=0:
            self.looper_run(4)

    def boton_flash_5(self, value):
        if value!=0:
            self.looper_run(5)

    def boton_flash_6(self, value):
        if value!=0:
            self.looper_run(6)

    def boton_flash_7(self, value):
        if value!=0:
            self.looper_run(7)

    def boton_flash_8(self, value):
        if value!=0:
            self.looper_run(8)

    def boton_flash_9(self, value):
        if value!=0:
            self.looper_run(9)

    def boton_flash_10(self, value):
        if value!=0:
            self.looper_run(10)

    def boton_flash_11(self, value):
        if value!=0:
            self.looper_run(11)

    def boton_flash_12(self, value):
        if value!=0:
            self.looper_run(12)

    #Stop buttons


    def boton_stop_1(self, value):
        if value!=0:
            self.looper_stop(1)

    def boton_stop_2(self, value):
        if value!=0:
            self.looper_stop(2)

    def boton_stop_3(self, value):
        if value!=0:
            self.looper_stop(3)

    def boton_stop_4(self, value):
        if value!=0:
            self.looper_stop(4)

    def boton_stop_5(self, value):
        if value!=0:
            self.looper_stop(5)

    def boton_stop_6(self, value):
        if value!=0:
            self.looper_stop(6)

    def boton_stop_7(self, value):
        if value!=0:
            self.looper_stop(7)

    def boton_stop_8(self, value):
        if value!=0:
            self.looper_stop(8)

    def boton_stop_8(self, value):
        if value!=0:
            self.looper_stop(8)

    def boton_stop_9(self, value):
        if value!=0:
            self.looper_stop(9)

    def boton_stop_10(self, value):
        if value!=0:
            self.looper_stop(10)

    def boton_stop_11(self, value):
        if value!=0:
            self.looper_stop(11)

    def boton_stop_12(self, value):
        if value!=0:
            self.looper_stop(12)

    #Undo buttons

    def boton_undo_current(self, value):
        if value!=0:
            self.undo_current()

    def boton_undo_1(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 1)

    def boton_undo_2(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 2)

    def boton_undo_3(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 3)

    def boton_undo_4(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 4)

    def boton_undo_5(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 5)

    def boton_undo_6(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 6)

    def boton_undo_7(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 7)

    def boton_undo_8(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 8)

    def boton_undo_9(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 9)

    def boton_undo_10(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 10)

    def boton_undo_11(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 11)

    def boton_undo_12(self, value):
        if value!=0:
            self.undo(MASTER['current_bank'], 12)

    #Auto-Overdub buttons

    def boton_auto_overdub_current(self, value):
        if value!=0:
            self.auto_ovedub_current()
            self.auto_ovedub_current()


    def boton_auto_overdub_1(self, value):
        if value!=0:
            self.auto_ovedub(1)
            self.auto_ovedub(1)

    def boton_auto_overdub_2(self, value):
        if value!=0:
            self.auto_ovedub(2)
            self.auto_ovedub(2)

    def boton_auto_overdub_3(self, value):
        if value!=0:
            self.auto_ovedub(3)
            self.auto_ovedub(3)

    def boton_auto_overdub_4(self, value):
        if value!=0:
            self.auto_ovedub(4)
            self.auto_ovedub(4)

    def boton_auto_overdub_5(self, value):
        if value!=0:
            self.auto_ovedub(5)
            self.auto_ovedub(5)

    def boton_auto_overdub_6(self, value):
        if value!=0:
            self.auto_ovedub(6)
            self.auto_ovedub(6)

    def boton_auto_overdub_7(self, value):
        if value!=0:
            self.auto_ovedub(7)
            self.auto_ovedub(7)

    def boton_auto_overdub_8(self, value):
        if value!=0:
            self.auto_ovedub(8)
            self.auto_ovedub(8)

    def boton_auto_overdub_9(self, value):
        if value!=0:
            self.auto_ovedub(9)
            self.auto_ovedub(9)

    def boton_auto_overdub_10(self, value):
        if value!=0:
            self.auto_ovedub(10)
            self.auto_ovedub(10)

    def boton_auto_overdub_11(self, value):
        if value!=0:
            self.auto_ovedub(11)
            self.auto_ovedub(11)

    def boton_auto_overdub_12(self, value):
        if value!=0:
            self.auto_ovedub(12)
            self.auto_ovedub(12)

    #Definicion de funciones



    def select_bank(self, bank):
        MASTER['previous_bank']=MASTER['current_bank']
        MASTER['current_bank']=bank
        #self.imprime('BANCO ACTUAL(selectbank)=' + str(MASTER['current_bank']))
        #self.imprime('BANCO PREVIO(selectbank)=' + str(MASTER['previous_bank']))

    def change_to_bank(self, bank):
        MASTER['pause']=True
        previous_bank=MASTER['previous_bank']
        if self.bank_is_empty(bank)==False:
            MASTER['pause']=False
            #self.imprime('BANCO ' + str(bank) + ' USADO')
        else:
            for a in range(MASTER['loopers']):
                lp=a+1
                if self.looper_is_recording(previous_bank, lp)==True:
                    MASTER['pause']=False
                else:
                    pass

        if MASTER['pause']==False:
            if bank==previous_bank:

                self.all_loopers_play(bank)
                #self.imprime('MISMO BANCO')
            else:

                for n in range(MASTER['loopers']):
                    lpr=n+1
                    self.get_current_layer(bank, lpr)
                    layer=MASTER[bank][lpr]['current_layer']
                    self.get_current_layer(previous_bank, lpr)
                    previous_layer=MASTER[previous_bank][lpr]['current_layer']

                    if self.looper_is_empty(previous_bank, lpr)==False: #Si el looper del banco anterior esta usado y NO esta en PAUSE
                        self.looper_stop(lpr)
                        if self.looper_is_recording(previous_bank, lpr)==True: #Comprueba si el looper del banco anterior estaba grabando
                                #self.imprime('BANK ' + str(previous_bank) + ' LOOPER ' + str(lpr) + ' ESTABA GRABANDO EN LAYER ' + str(previous_layer) )
                                self.looper_forward(bank, lpr)

                    if self.looper_is_empty(bank, lpr)==False: #Si el banco de destino NO esta vacio
                        if self.looper_is_recording(previous_bank, lpr)==False:
                                self.looper_forward(bank, lpr)
                                #self.imprime('CURRENT LOOPER=' + str(MASTER['current_looper']))


        if MASTER['pause']==False:
            MASTER['previous_bank']=bank

    def all_loopers_play(self, bank):
        for n in range(MASTER['loopers']):
            lp=n+1
            #self.imprime('MISMO LOOPER - lp' + str(lp))
            if self.looper_is_empty(bank, lp)==False:
                #self.imprime('PASE 1')
                if self.looper_is_recording(bank, lp)==True:
                    #self.imprime('PASE 2')
                    self.looper_run(lp)
                    pass
                else:
                    layer=MASTER[bank][lp]['current_layer']
                    x, y=self.get_position(bank, lp, layer)
                    self.song().tracks[x].clip_slots[y].fire()
                    #self.imprime('PASE 3')

    def looper_run(self, looper, bank=None, keep_current_looper=False):
        if bank==None:
            bank=MASTER['current_bank']

        self.get_current_layer(bank, looper)

        #Condition for if PAUSE was activated (postponed record after a bank change)
        if MASTER['pause']==True:
            MASTER['pause']=False
            #self.imprime('LINEA 508')
            for n in range(MASTER['loopers']):
                lpr=n+1
                previous_bank=MASTER['previous_bank']
                previous_layer=MASTER[previous_bank][lpr]['current_layer']
                x, y=self.get_position(previous_bank, lpr, previous_layer)
                self.song().tracks[x].stop_all_clips()

        self.looper_forward(bank, looper)
        if keep_current_looper==False:
            MASTER['current_looper']=looper
            if looper!=MASTER['previous_looper']:
                MASTER['previous_looper']=looper

    def looper_forward(self, bank, looper, keep_current_looper=False):
        AUTO_RECORD_THROUGH_LOOPERS=True #Option for enabling record through loopers
        layer=MASTER[bank][looper]['current_layer']
        track=MASTER[bank][looper][layer]['track']
        clip=MASTER[bank][looper][layer]['clip_slot']
        t=track-1
        c=clip-1
        #self.arm(t)

        self.focus(bank, looper, layer)


        if self.song().tracks[t].clip_slots[c].is_playing:
            if self.song().tracks[t].clip_slots[c].is_recording:

                self.song().tracks[t].clip_slots[c].fire()
                if not MASTER[bank][looper]['current_layer'] <=1:
                    MASTER[bank][looper]['current_layer'] -=1
                    layer=MASTER[bank][looper]['current_layer']
                    track=MASTER[bank][looper][layer]['track']
                    clip=MASTER[bank][looper][layer]['clip_slot']
                    t=track-1
                    c=clip-1
                    self.song().tracks[t].stop_all_clips()
                    MASTER[bank][looper]['current_layer'] +=1
            else:
                if MASTER[bank][looper]['current_layer'] < MASTER['layers']:
                    MASTER[bank][looper]['current_layer'] +=1
                    self.looper_forward(bank, looper)

        else:
            self.song().tracks[t].clip_slots[c].fire()

        if AUTO_RECORD_THROUGH_LOOPERS==True:
                lpr=MASTER['previous_looper']
                layer=MASTER[bank][lpr]['current_layer']
                track=MASTER[bank][lpr][layer]['track']-1
                clip=MASTER[bank][lpr][layer]['clip_slot']
                t=track-1
                c=clip-1
                if self.song().tracks[t].clip_slots[c].is_recording:
                    self.song().tracks[t].clip_slots[c].fire()
                    #MASTER[bank][looper]['current_layer'] +=1
                    if keep_current_looper==False:
                        MASTER['current_looper']=looper

    def undo(self, bank, looper):
        x, y=self.get_position(bank, looper, MASTER[bank][looper]['current_layer'])
        #self.imprime(str(x)+' - '+str(y))
        if self.song().tracks[x].clip_slots[y].has_clip:
            self.song().tracks[x].clip_slots[y].delete_clip()
        if MASTER[bank][looper]['current_layer']>1:
            x, y=self.get_position(bank, looper, MASTER[bank][looper]['current_layer']-1)
            if not self.song().tracks[x].clip_slots[y].is_playing:
                self.song().tracks[x].clip_slots[y].fire()
            if MASTER[bank][looper]['current_layer'] >1:
                MASTER[bank][looper]['current_layer'] -=1

    def undo_current(self):
        bank=MASTER['current_bank']
        looper=MASTER['current_looper']
        x, y=self.get_position(bank, looper, MASTER[bank][looper]['current_layer'])
        #self.imprime(str(x)+' - '+str(y))
        if self.song().tracks[x].clip_slots[y].has_clip:
            self.song().tracks[x].clip_slots[y].delete_clip()
        if MASTER[bank][looper]['current_layer']>1:
            x, y=self.get_position(bank, looper, MASTER[bank][looper]['current_layer']-1)
            if not self.song().tracks[x].clip_slots[y].is_playing:
                self.song().tracks[x].clip_slots[y].fire()
            if MASTER[bank][looper]['current_layer'] >1:
                MASTER[bank][looper]['current_layer'] -=1

    def looper_stop(self, looper):
        bank=MASTER['current_bank']
        x=MASTER[bank][looper][1]['track']-1
        self.song().tracks[x].stop_all_clips()
        x=MASTER[bank][looper][2]['track']-1
        self.song().tracks[x].stop_all_clips()

    def all_loopers_stop(self):
        banks=MASTER['banks']
        loopers=MASTER['loopers']
        #track, clip_slot=self.get_position()
        #self.imprime('BANKS:' + str(banks))
        #self.imprime('LOOPERS:' + str(loopers))
        for n in range(loopers):
            #self.imprime('STOP:' + str(n+1))

            ta=MASTER[1][n+1][1]['track']-1
            tb=MASTER[1][n+1][2]['track']-1
            bank=MASTER['current_bank']
            looper=MASTER['current_looper']

            x, y=self.get_position(bank, looper, MASTER[bank][looper]['current_layer'])

            if not self.song().tracks[x].clip_slots[y].is_recording:
                self.song().tracks[ta].stop_all_clips()
                self.song().tracks[tb].stop_all_clips()

    def auto_ovedub_current(self):
        bank=MASTER['current_bank']
        looper=MASTER['current_looper']
        layer=MASTER[bank][looper]['current_layer']
        track=MASTER[bank][looper][layer]['track']
        clip=MASTER[bank][looper][layer]['clip_slot']
        t=track-1
        c=clip-1
        self.arm(t)
        #self.imprime('pulsado OD')
        #self.imprime(bank)
        #self.imprime(looper)
        if self.song().tracks[t].clip_slots[c].is_playing:
            if self.song().tracks[t].clip_slots[c].is_recording:

                self.song().tracks[t].clip_slots[c].fire()
                if not MASTER[bank][looper]['current_layer'] <=1:
                    MASTER[bank][looper]['current_layer'] -=1
                    layer=MASTER[bank][looper]['current_layer']
                    track=MASTER[bank][looper][layer]['track']
                    clip=MASTER[bank][looper][layer]['clip_slot']
                    t=track-1
                    c=clip-1
                    #self.song().tracks[t].stop_all_clips()
                    MASTER[bank][looper]['current_layer'] +=1

            MASTER[bank][looper]['current_layer'] +=1
            self.looper_forward(bank, looper)
        else:
            self.song().tracks[t].clip_slots[c].fire()

    def auto_ovedub(self, looper):
        bank=MASTER['current_bank']
        layer=MASTER[bank][looper]['current_layer']
        track=MASTER[bank][looper][layer]['track']
        clip=MASTER[bank][looper][layer]['clip_slot']
        t=track-1
        c=clip-1
        self.arm(t)
        #self.imprime('pulsado OD')
        #self.imprime(bank)
        #self.imprime(looper)
        if self.song().tracks[t].clip_slots[c].is_playing:
            if self.song().tracks[t].clip_slots[c].is_recording:

                self.song().tracks[t].clip_slots[c].fire()
                if not MASTER[bank][looper]['current_layer'] <=1:
                    MASTER[bank][looper]['current_layer'] -=1
                    layer=MASTER[bank][looper]['current_layer']
                    track=MASTER[bank][looper][layer]['track']
                    clip=MASTER[bank][looper][layer]['clip_slot']
                    t=track-1
                    c=clip-1
                    #self.song().tracks[t].stop_all_clips()
                    MASTER[bank][looper]['current_layer'] +=1

            MASTER[bank][looper]['current_layer'] +=1
            self.looper_forward(bank, looper)
        else:
            self.song().tracks[t].clip_slots[c].fire()

    def bank_is_empty(self, bank): #True if empty, False if used
        bank_is_empty=True
        for n in range(MASTER['loopers']):
            lpr=n+1
            self.get_current_layer(bank, lpr)
            layer=MASTER[bank][lpr]['current_layer']
            x, y=self.get_position(bank, lpr, layer)
            if self.song().tracks[x].clip_slots[y].has_clip:
                bank_is_empty=False
        return bank_is_empty

    def looper_is_empty(self, bank, looper):
        looper_is_empty=True
        self.get_current_layer(bank, looper)
        layer=MASTER[bank][looper]['current_layer']
        x, y=self.get_position(bank, looper, layer)
        if self.song().tracks[x].clip_slots[y].has_clip:
            looper_is_empty=False
            #self.imprime('BANK ' + str(bank)+ ' LOOPER ' + str(looper) + ' USADO')
        else:
            #self.imprime('BANK ' + str(bank)+ ' LOOPER ' + str(looper) + ' VACIO')
            pass
        return looper_is_empty

    def looper_is_recording(self, bank, looper):
        looper_is_recording=False
        layer=MASTER[bank][looper]['current_layer']
        x, y=self.get_position(bank, looper, layer)
        if self.song().tracks[x].clip_slots[y].is_recording:
            looper_is_recording=True
            #self.imprime('BANK ' + str(bank)+ ' LOOPER ' + str(looper) + ' GRABANDO')
        #else:
            #self.imprime('BANK ' + str(bank)+ ' LOOPER ' + str(looper) + ' NO ESTA GRABANDO')
        return looper_is_recording

    def get_position(self, bank, looper, layer):
        x=MASTER[bank][looper][layer]['track']
        y=MASTER[bank][looper][layer]['clip_slot']
        return x-1, y-1

    def get_current_layer(self, bank, looper):
        #self.imprime('pulsado REFRESH')

        for v in MASTER[bank][looper]:
            #self.imprime('LAYER_' + str(v))
            try:
                x,y=self.get_position(bank,looper,v)
                if self.song().tracks[x].clip_slots[y].has_clip:
                    MASTER[bank][looper]['current_layer']=v
                    #self.imprime('tiene_clip_' + str(v))
            except: pass

        return MASTER[bank][looper]['current_layer']

    def focus(self, bank, looper, layer):
        x, y=self.get_position(bank, looper, layer)

        selected_track = self.song().view.selected_track
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        all_scenes = tuple(self.song().scenes)
        self.song().view.selected_track = all_tracks[x]
        self.song().view.selected_scene = all_scenes[y]

    def gui_focus(self, track, clip):
        selected_track = self.song().view.selected_track
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        all_scenes = tuple(self.song().scenes)
        self.song().view.selected_track = all_tracks[track]
        self.song().view.selected_scene = all_scenes[clip]

    def arm(self, track):
        self.song().tracks[track].arm=True

    def disarm(self, track):
        self.song().tracks[track].arm=False

    def send_midi_out(self, midi_ch, note=0):
        note_on=144+MIDI_CHANNEL
        note_off=128+MIDI_CHANNEL
        self._send_midi((note_on,note,127))
        self._send_midi((note_off,note,0))
        self.imprime('Mandado NOTE ON/OFF (127-0) midi out: Channel ' + str(MIDI_CH) + ' nota ' + str(note) )

    def copy(self, track, clip):
        #self.imprime('PULSADO Copy')
        self.gui_focus(track, clip)
        self.send_midi_out(MIDI_CHANNEL, 6)

    def cut(self, track, clip):
        #self.imprime('PULSADO Cut')
        self.gui_focus(track, clip)
        self.send_midi_out(MIDI_CHANNEL, 7)

    def paste(self, track, clip):
        #self.imprime('PULSADO Paste')
        self.gui_focus(track, clip)
        self.send_midi_out(MIDI_CHANNEL, 8)

    #def create_session_control(self):
        #escenas_por_banco=self.detecta_numero_escenas_por_banco()
        #width=48                           #width of the Session
        #height=escenas_por_banco                     #height of the Session
        #self.Session=SessionComponent(width,height)          #here we create a session called Session
        #self.Session.set_offsets(0,0)       #offset start a the up-left corner (track1,row1)
        #self.Session._do_show_highlight()   #to ensure that this session will be highlighted

    def imprime(self, args):
        self.log_message('====' + str(args))

    def scan(self):
        total_pistas=self.detecta_numero_pistas()
        escenas_por_banco=self.detecta_numero_escenas_por_banco()

        #Create all the clips
        for n in range(BANCOS):
            ban=n+1
            for m in range(total_pistas):
                pis=m+1
                for p in range(escenas_por_banco*2):
                    lay=p+1
                    conv=str('LOOPER_' + str(ban) + '_' + str(pis) +'_' + str(lay) + ' = ' + str(DEFINICION))
                    exec(str(conv))

        #Separate all the clips through layers, the tracks and banks
        for a in range(BANCOS):
            ban=a+1
            conv=str('BANK'+str(ban)+'={}')
            exec str(conv)
            for b in range(total_pistas):
                pis=b+1
                conv=str('BANK' + str(ban) +'[' + str(pis) + ']={}')
                exec str(conv)
                for p in range(escenas_por_banco*2):
                    lay=p+1
                    conv=str('BANK'+ str(ban) + '[' + str(pis) + '][' + str(lay) + '] =  LOOPER_' + str(ban) + '_' + str(pis) + '_' + str(lay))
                    exec(str(conv))

        #Create MASTER with the results
        for d in range(BANCOS):
            ban=d+1
            conv='MASTER['+str(ban)+']= BANK' + str(ban)
            exec(str(conv))


        MASTER['limits']=0
        MASTER['current_bank']=1
        MASTER['previous_bank']=1
        MASTER['banks']=BANCOS
        MASTER['loopers']=total_pistas
        MASTER['layers']=escenas_por_banco*2
        MASTER['current_looper']=1
        MASTER['previous_looper']=1
        MASTER['pause']=False

        self.detecta_numero_pistas(get_track_numbers=True)

        for z in MASTER:
            try:
                for x in MASTER[z]:
                    try:
                        for w in MASTER[z][x]:
                            MASTER[z][x]['current_layer']=1
                    except: pass
            except: pass

        for num in MASTER:
            try:
                for bum in MASTER[num]:
                    try:
                        #self.imprime('RESULTADO BANCO-' + str(num) + '-LOOPER-' + str(bum) + str(MASTER[num][bum]))
                        pass
                    except: pass
            except: pass

        self.mensaje('FINALIZADO SCAN - BANCOS: ' + str(MASTER['banks']) + ' - LOOPERS: ' + str(MASTER['loopers']) + ' - LAYERS per LOOPER: '+ str(MASTER['layers']))


    def detecta_numero_escenas_por_banco(self): #Gets the number of scenes per bank and returns nopcb value (INT)
        #Detecta el numero de escenas
        b=0
        for a in self.song().tracks[1].clip_slots:
            b+=1
        total_escenas=b

        nspb = total_escenas/BANCOS
        return nspb

    def detecta_numero_pistas(self, get_track_numbers=False): #Gets the number of loopers and returns total_pistas value (INT)
        #Escanea el proyecto en busca de las pistas loopers
        total_pistas=''
        a=0
        b=0
        ca=0
        cb=0

        for d in range(len(self.song().tracks)):
            e=d+1
            mens_in=self.song().tracks[d].name

            #self.imprime(mens_in)

            mens_a='LP'+str(a+1)+'a'
            mens_b='LP'+str(b+1)+'b'

            if str(mens_in)==str(mens_a):
                    a+=1
                    if get_track_numbers:
                            BANCOS=MASTER['banks']
                            nspb=self.detecta_numero_escenas_por_banco()
                            for x in MASTER:
                                try:
                                    ca=0
                                    for n in MASTER[x][a]:
                                        try:
                                            if n%2 != 0:
                                                ca+=1
                                                MASTER[x][a][n]['track'] = e
                                                MASTER[x][a][n]['clip_slot'] = (nspb*(x-1))+ca
                                        except: pass
                                except: pass

            if str(mens_in)==str(mens_b):
                    b+=1
                    if get_track_numbers:
                            BANCOS=MASTER['banks']
                            nspb=self.detecta_numero_escenas_por_banco()
                            for z in MASTER:
                                try:
                                    cb=0
                                    for m in MASTER[z][b]:
                                        try:
                                            if m%2 == 0:
                                                cb+=1
                                                MASTER[z][b][m]['track'] = e
                                                MASTER[z][b][m]['clip_slot'] = (nspb*(z-1))+cb
                                        except: pass
                                except: pass

        if a==b:
            total_pistas=a

        return total_pistas

