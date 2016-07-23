#by Nikolasi
from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eDVBCI_UI, eDVBCIInterfaces
from Poll import Poll

class ModuleControl(Poll, Converter, object):
	NAME1 = 0
	NAME2 = 1
	NAME3 = 2
	NAME4 = 3
	PICON1 = 4
	PICON2 = 5
	PICON3 = 6
	PICON4 = 7
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)		
		if type == "NameSlot1":
			self.type = self.NAME1
		elif type == "NameSlot2":
			self.type = self.NAME2
		elif type == "NameSlot3":
			self.type = self.NAME3
		elif type == "NameSlot4":
			self.type = self.NAME4			
		elif type == "PiconSlot1":
			self.type = self.PICON1
		elif type == "PiconSlot2":
			self.type = self.PICON2
		elif type == "PiconSlot3":
			self.type = self.PICON3
		elif type == "PiconSlot4":
			self.type = self.PICON4
		self.poll_interval = 1000
		self.poll_enabled = True
		
        def getFilename(self, state, slot):
            name = ''
	    if state == 0:
		name = _("Slot %d") %(slot+1) + " - " + _("no module found") 
	    elif state == 1:
		name = _("Slot %d") %(slot+1) + " - " + _("init modules")
	    elif state == 2:
		name = _("Slot %d") %(slot+1) + " - " + eDVBCI_UI.getInstance().getAppName(slot)	
            return name

        def getPiconname(self, state, slot):
            name = ''
	    if state == 0:
		name = "NOMODULE_SLOT%d" %(slot)
	    elif state == 1:
		name = "INITMODULE_SLOT%d" %(slot)
	    elif state == 2:
		name = "READY_SLOT%d" %(slot)              
            return name	 			

	@cached
	def getText(self):
                name = ""
                service = self.source.service
                if service:
                    NUM_CI=eDVBCIInterfaces.getInstance().getNumOfSlots()
                    if NUM_CI > 0:
                        self.control = True
		    else:
			self.control = False
		else:
			self.control = False			
		if self.type == self.NAME1:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(0)
                                if state != -1:
	                            name = self.getFilename(state, 0)
	                        else:
		                        name = _("Slot %d") %(1) + " - " + _("no module found") 
		        else:
		              name = _("Slot %d") %(1) + " - " + _("no module found")			              
			return name
		elif self.type == self.NAME2:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(1)
                                if state != -1:
	                            name = self.getFilename(state, 1)
	                        else:
		                        name = _("Slot %d") %(2) + " - " + _("no module found") 
		        else:
		              name = _("Slot %d") %(2) + " - " + _("no module found")                  
			return name
		elif self.type == self.NAME3:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(2)
                                if state != -1:
	                            name = self.getFilename(state, 2)
	                        else:
		                        name = _("Slot %d") %(3) + " - " + _("no module found") 
		        else:
		              name = _("Slot %d") %(3) + " - " + _("no module found")                  
			return name
		elif self.type == self.NAME4:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(3)
                                if state != -1:
	                            name = self.getFilename(state, 3)
	                        else:
		                        name = _("Slot %d") %(4) + " - " + _("no module found") 
		        else:
		              name =  _("Slot %d") %(4) + " - " + _("no module found")                
			return name
		elif self.type == self.PICON1:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(0)
                                if state != -1:
	                            name = self.getPiconname(state, 1)
	                        else:
		                        name = "NOMODULE_SLOT1"
		        else:
		              name = "NOMODULE_SLOT1"                 
			return name
		elif self.type == self.PICON2:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(1)
                                if state != -1:
	                            name = self.getPiconname(state, 2)
	                        else:
		                        name = "NOMODULE_SLOT2"
		        else:
		              name = "NOMODULE_SLOT2"                 
			return name
		elif self.type == self.PICON3:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(2)
                                if state != -1:
	                            name = self.getPiconname(state, 3)
	                        else:
		                        name = "NOMODULE_SLOT3"
		        else:
		              name = "NOMODULE_SLOT3"                 
			return name
		elif self.type == self.PICON4:
                        if self.control:
                                state = eDVBCI_UI.getInstance().getState(3)
                                if state != -1:
	                            name = self.getPiconname(state, 4)
	                        else:
		                        name = "NOMODULE_SLOT4"
		        else:
		              name = "NOMODULE_SLOT4"                 
			return name		       
	        return ""	
	text = property(getText)	

	def changed(self, what):
		Converter.changed(self, (self.CHANGED_POLL,))
