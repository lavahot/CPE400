#ROUTER CLASS
#Zachary Carlson
#Thomas 'Taylor' Mansfield
#MacCallister Higgins
#CPE 400 Project 2

class Router():
	"""Router Class"""
	def __eq__(self, other):
		"""Equality only checks router ids"""
		return self.ip == other.ip #Router IP

	def __init__(self, ip, table = {}, neighbors = []):
		self.ip = ip #Router IP 
		self.neighbors = []#List of neighbor's IP Addresses
		self.ripTable = {"Destination Subnet": ["Next Router", "Number of Hops"]} #RIP Table Subnets end in 0
		self.ripTableCap = 25 #Maximum number of rows allowed in the RIP Table
		self.hopCap = 15
		self.bAdvertising = True
		self.bUpdated = False
		self.buffer = []#list of packets that represents it's buffer
		if table:
			for row in table:
				if len(table[row]) == 2:
					self.addRipRow(row, table[row][0], table[row][1] )
		
	def addRipRow(self, subnet, nextR, hops):
		"""Adds row to table and updates neighbors if needed"""
		#ensure table isn't over the cap and that hops are under hopCap
		if len(self.ripTable) <= self.ripTableCap and hops < self.hopCap:
			#update neighbors if needed
			if hops == 2 and nextR not in self.neighbors:
				self.addNeighbor(nextR)
			self.ripTable[subnet] = [nextR, hops]
			return True
		else:
			return False
	
	def addNeighbor(self, neighborIP):
		"""adds the neighborIP to the list of neighbors"""
		#add neighbor to list		
		if neighborIP not in self.neighbors:
			self.neighbors.append(neighborIP)
	def advertise(self, neighbor):
		"""Will send out an advertisement to the connected neighbor if that neighbor is in fact a valid neighbor"""
		#check if neighbor is valid
		if neighbor.ip in self.neighbors:
			nUpdate=False #new bool
			#foreach destination subnet in the destinations of the router
			for subnet in self.ripTable:
				#if this subnet is not in their particular table, it looks into their table and adds a hop
				if not neighbor.ripTable[subnet]:
					neighbor.ripTable[subnet] = [self.ip, self.ripTable[subnet][1] + 1]
					nUpdate = True
				#if the router you are connected to doesn't have a better route, fix it 
				elif neighbor.ripTable[subnet][1] > self.ripTable[subnet][1] + 1:
					neighbor.ripTable[subnet] = [self.ip, self.ripTable[subnet][1] + 1]
					nUpdate = True
			#if nUpdate=True
			if nUpdate:
				#mark it as updated and set it to advertise
				neighbor.bUpdated = True
				neighbor.bAdvertising = True

	#def advertise(self, router):
	#	for subnet in self.netMap[router][0]: #foreach destination in the dictionary of destinations of the router
	#		if subnet not in self.netMap[neighbor][0]: #if this subnet is not in their particular table, it looks into their table and adds a hop
	#			self.netMap[neighbor][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1) 
	#			nUpdate=True
	#		elif self.netMap[neighbor][0][subnet][1] > self.netMap[router][0][subnet][1] + 1: #if the router you are connected to doesn't have a better route, fix it  
	#			self.netMap[neighbor][0][subnet] = (router,self.netMap[router][0][subnet][1] + 1)
	#			nUpdate=True
	#	if nUpdate:
	#		self.netMap[neighbor].bUpdates=True #mark it as updated
	#	self.netMap[router].bUpdated=False #marks current router as no longer advertising
