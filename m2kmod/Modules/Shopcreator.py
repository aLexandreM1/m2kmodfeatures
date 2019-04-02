import ui,app,chat,chr,net,player,item,skill,time,game,shop,chrmgr
import background,constInfo,wndMgr,math,uiCommon,grp,dbg,m2k_lib

ListOfItems = [ [ 0 for x in xrange(2) ] for x in xrange(50) ]

class ShopDialog(ui.ScriptWindow):
	
	Gui = {}
	
	def __init__(self):
		self.Board = ui.ThinBoard() 
		self.Board.SetPosition(52, 40)
		self.Board.SetSize(350, 370)
	#	self.Board.AddFlag('movable')
		self.Board.Hide()
		
		self.comp = m2k_lib.Component()
		self.Header = self.comp.TextLine(self.Board, 'Shop-Creator', 145, 8, self.comp.RGB(255, 255, 0))
		self.Name = self.comp.TextLine(self.Board, 'Shop-Name:', 30, 310, self.comp.RGB(0, 229, 650))
	
		self.CloseButton = self.comp.Button(self.Board, '', 'Close', 329, 8, self.Hide_UI, 'd:/ymir work/ui/public/close_button_01.sub', 'd:/ymir work/ui/public/close_button_02.sub', 'd:/ymir work/ui/public/close_button_03.sub')
		self.MultiplicationButton = self.comp.Button(self.Board, 'Multiplication', '', 203, 340, self.SetMultiplication, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub','d:/ymir work/ui/public/large_button_03.sub')
		self.MakeShopButton = self.comp.Button(self.Board, 'Make Shop', '', 61, 340, self.CreateShop, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub','d:/ymir work/ui/public/large_button_03.sub')
		self.ShopNameSlotbar, self.ShopNameEditline = self.comp.EditLine(self.Board, '', 100, 310, 220, 18, 34)
		
		iX = 82
		eX = 10
		y = 30
		for line in xrange(20):
			self.Gui["Item"+str(line+1)] = self.comp.TextLine(self.Board, 'Item'+str(line+1), iX, y, self.comp.RGB(0, 229, 650))
			self.Gui["ItemPriceSlotBar"+str(line+1)], self.Gui["ItemPriceEditline"+str(line+1)] = self.comp.EditLine(self.Board, '0', eX, y, 67, 18, 9)
			y+=25
			if y == 280:
				y = 30
				iX = 257
				eX = 185
				
		self.ShopNameEditline.SetText(m2k_lib.ReadConfig("ShopName"))
		self.Multiplication = int(m2k_lib.ReadConfig("Multiplication"))
		
		if self.Multiplication:
			self.MultiplicationButton.SetText('Multiplication')
		else:
			self.MultiplicationButton.SetText('No Multiplication')
		
	#	for i in xrange(20):
	#		exec 'self.Gui["ItemPriceEditline'+ str(i+1) + '"]' + '.SetText("' + GetPrice(i) + '")'
	#	
	#	self.GetItems()	
		
	def switch_state(self):
		if self.Board.IsShow():
			self.Hide_UI()
		else:
			self.Shopw_UI()
	def Shopw_UI(self):
		self.Board.Show()
		for line in xrange(20):
			self.Gui["Item"+str(line+1)].Show()
			self.Gui["ItemPriceSlotBar"+str(line+1)].Show()
		for i in xrange(20):
			exec 'self.Gui["ItemPriceEditline'+ str(i+1) + '"]' + '.SetText("' + GetPrice(i) + '")'
		self.GetItems()		
		
	def Hide_UI(self):
		self.Board.Hide()
		m2k_lib.SaveConfig("ShopName", str(self.ShopNameEditline.GetText()))
		m2k_lib.SaveConfig("Multiplication", str(self.Multiplication))
		for i in xrange(20):
			exec 'SavePrice("price' + str(i+1)+'", str(self.Gui["ItemPriceEditline' + str(i+1) + '"]' + '.GetText()))'
	

	def SetMultiplication(self):
		if self.Multiplication:
			self.Multiplication = 0
			self.MultiplicationButton.SetText('No Multiplication')
			chat.AppendChat(7, '[m2k-Mod] Multiplication changed to no price nultiplication')
		else: 
			self.Multiplication = 1
			self.MultiplicationButton.SetText('Multiplication')
			chat.AppendChat(7, '[m2k-Mod] No price multiplication changed to multiplication')
		
	
	def CreateShop(self):
		price = 0
		for i in xrange(0, 40):
			ItemValue = player.GetItemIndex(i)
			if ItemValue == 50300:
				ItemValue = 100000 + player.GetItemMetinSocket(i, 0)
			if ItemValue != 0:
				for j in xrange(0,19):
					if ItemValue == ListOfItems[j][0]:
						exec 'price = int(self.Gui["ItemPriceEditline' + str(j+1) + '"]' + '.GetText())'
				if self.Multiplication:
					newPrice = int(price) * player.GetItemCount(i)
				else:
					newPrice = int(price)
				if int(newPrice) != 0:
					shop.AddPrivateShopItemStock(player.SLOT_TYPE_INVENTORY, int(i), int(i), int(newPrice))
				else:
					chat.AppendChat(7, '[m2k-Mod] Item not added to the Stock because of Price = 0')
		shop.BuildPrivateShop(self.ShopNameEditline.GetText())
		
	def GetItems(self):
		for ra in xrange(0,40):
			ListOfItems[ra][0] = 0
		for ri in xrange(0,40):
			disable = 0
			ItemValue = player.GetItemIndex(ri)
			if ((int(ItemValue) != 0) and (ItemValue != 50300)):
				item.SelectItem(ItemValue)
				for i in xrange(0,29):
					if (ListOfItems[i][0] == ItemValue):
						disable = 1
						break
					else:
						disable = 0
				if (disable == 0):
					for j in xrange(0,29):
						if (ListOfItems[j][0] == 0):
							ListOfItems[j][0] = ItemValue
							exec 'self.Gui["Item'+ str(j + 1) + '"]' + '.SetText("' + item.GetItemName() + '")'
							break
			if (ItemValue == 50300):
				sbId = player.GetItemMetinSocket(ri, 0)
				ItemValue = 100000 + sbId
				disable = 0
				for i in xrange(0, 19):
					if (ListOfItems[i][0] == ItemValue):
						disable = 1
						break
					else:
						disable = 0
				if (disable == 0):
					for j in xrange(0, 19):
						if (ListOfItems[j][0] == 0):
							ListOfItems[j][0] = ItemValue
							exec 'self.Gui["Item' + str(j + 1) + '"]' + '.SetText("' + str(skill.GetSkillName(sbId)) + '")'
							break
		CountItems = 0
		for hid in xrange(0, 20):
			if (ListOfItems[hid][0] == 0):
				exec 'self.Gui["Item' + str(hid+1) + '"]' + '.Hide()'
				exec 'self.Gui["ItemPriceSlotBar' + str(hid+1) + '"]' + '.Hide()'
			if (ListOfItems[hid][0] != 0):
				CountItems += 1

def GetPrice(line):
	handle = app.OpenTextFile('m2kmod/Saves/priceconfig.m2k')
	t = app.GetTextFileLine(handle, line)
	return t.split('=')[1]
		
def SavePrice(Setting, Value):
	sReader = open('m2kmod/Saves/priceconfig.m2k', 'r')
	sLines = file.readlines(sReader)
	sWriter = open('m2kmod/Saves/priceconfig.m2k', 'w')
	for Line in sLines:
		if Line.startswith(Setting + '='):
			Line = Setting + '=' + Value + '\n'
		sWriter.write(Line)
