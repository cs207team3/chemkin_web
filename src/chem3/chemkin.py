"""
This is a chemical kinetics module which can be used to calculate the reaction
rate of a system of elementary, reversible and irreversible reactions.

Future updates are intended to address more reaciton types (duplicate,
three-body).

For more infomation regarding chemical kinetics, please visit:
https://en.wikipedia.org/wiki/Chemical_kinetics
"""
import numpy as np

class Reaction():
	"""Reaction Class for chemical kinetics calculations

	ATRIBUTES:
	=========
	reactants: dict of reaction reactant species
	products: dict of reaction product species
	reversible: boolean
	reac_type: reaction type (elementary, duplicate(not yet supported),
				three-body(not yet supported)
	reac_id: ID of reaction
	coef_type: Reaction rate coefficient (constant, Arrhenius, Modified Arrhenius)
	coef: dict of reaction rate variables {A, E, b, T}

	METHODS:
	=======
	.__init__: init attributes
	.__eq__: Two reactions are same if the only different
	attributes are their Ids
	.__ste__: Returns string representation of Reaction class
	.set_reac_coefs: sets reaction coefficients as Contant, Arrhenius or
	Modified Arrhenius
	.init_const_coef: returns k for constant reaction rate
	.init_arr_coef: returns Arrhenius reaction rate
	.init_marr_coef: returns Modified Arrhenius reaction rate

	EXAMPLES:
	========
	>>> reactants = {'O2': 1.0, 'H2': 2.0}
	>>> products = {'OH': 2.0, 'H2': 1.0}
	>>> coefs = {'E': 50000.0, 'b': 0.5, 'A': 100000000.0}
	>>> r1 = Reaction(reactants, products,
	...  		  False, 'Elementary', 'reaction01',
	...  		  'modifiedArrhenius', coefs)
	>>> type(r1)
	<class 'chem3.chemkin.Reaction'>
	>>> r1.set_reac_coefs(100)
	>>> r1.init_const_coef(5)
	5
	>>> r1.init_arr_coef(2, 3, 100) # Calculates the Arrhenius reaction rate coefficient
	1.9927962618542914

	"""
	def __init__(self, reactants, products, reversible, 
		         reac_type, reac_id, coef_type, coef, equation=''):
		"""Sets class attributes and returns reference of the class object

		INPUTS
		======
		reactants: 	dict
					Reactant species (str) and their coefficients (floats)
		products: 	dict
					Product species (str) and their coefficients (floats)
		reversible:	boolean
					Whether the reaction is reversible
		reac_type:	str
					Reaction type
		reac_id:	str
					Reaction id (normally read from .xml file)
		coef_type:  str
					Type of coefficients
					Must be either Constant, Arrhenius, or modifiedArrhenius
		coef:		dict
					Contains values of A, b, E
		equation:	str 
					Equation of the reation
					Optional
		"""
		self.reactants = reactants
		self.products = products
		self.reversible = reversible
		self.reac_type = reac_type
		self.reac_id = reac_id
		self.coef_type = coef_type
		self.coef = coef
		self.equation = equation

	def __eq__(self, other):
		"""Overrides equality operator:
		Two reactions are same if the only different
		attributes are their Ids
		"""
		return self.reactants == other.reactants \
			and self.products == other.products \
			and self.reversible == other.reversible \
			and self.reac_type == other.reac_type \
			and self.coef_type  == other.coef_type \
			and self.coef == other.coef \

	def __str__(self):
		"""Returns string representation of Reaction class"""
		return 'Reactants: ' + str(self.reactants) + \
			   '\nProducts: ' + str(self.products) + \
			   '\nReversible: ' + str(self.reversible) + \
			   '\nReaction Type: ' + self.reac_type + \
			   '\nReaction Id: ' + self.reac_id + \
			   '\nCoefficient Type: ' + self.coef_type + \
			   '\nCoefficients: ' + str(self.coef) + \
			   '\nEquation: ' + self.equation


	def set_reac_coefs(self, T):
		"""Sets reaction coefficients as:
		Constant, Arrhenius, or Modified Arrhenius

		INPUTS:
		======
		T: 	float
			Temperature
			Must be positive
		"""
		if self.coef_type == 'Constant':
			self.k = self.init_const_coef(self.coef['k'])
		elif self.coef_type == 'Arrhenius':
			self.k = self.init_arr_coef(self.coef['A'], self.coef['E'], T)
		elif self.coef_type == 'modifiedArrhenius':
			self.k = self.init_marr_coef(self.coef['A'], self.coef['b'], self.coef['E'], T)

	def init_const_coef(self, k):
		"""Returns a constant reaction rate coefficient

		INPUTS:
		=======
		k: float, default value = 1.0
		   Constant reaction rate coefficient

		RETURNS:
		========
		k: float
		   Constant reaction rate coefficient
		"""
		if k < 0:
			raise ValueError("Negative reaction rate coefficients are prohibited.")

		return k

	def init_arr_coef(self, A, E, T, R=8.314):
		"""Calculates the Arrhenius reaction rate coefficient

		INPUTS:
		=======
		A: float
		   Arrhenius prefactor
		   Must be positive
		E: float
		   Activation energy
		T: float
		   Temperature
		   Must be positive
		R: float, default value = 8.314
		   Ideal gas constant
		   Must be positive

		RETURNS:
		========
		k: float
		   Arrhenius reaction rate coefficient
		"""

		if A < 0.0:
			raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

		if T < 0.0:
			raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

		if R < 0.0:
			raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

		return A * np.exp(-E / R / T)

	def init_marr_coef(self, A, b, E, T, R=8.314):
		"""Calculates the modified Arrhenius reaction rate coefficient

		INPUTS:
		=======
		A: float
		   Arrhenius prefactor
		   Must be positive
		b: float
		   Modified Arrhenius parameter
		E: float
		   Activation energy
		T: float
		   Temperature
		   Must be positive
		R: float, default value = 8.314
		   Ideal gas constant
		   Must be positive

		RETURNS:
		========
		k: float
		   Modified Arrhenius reaction rate coefficient
		"""
		if A < 0.0:
			raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

		if T < 0.0:
			raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

		if R < 0.0:
			raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

		return A * (T**b) * np.exp(-E / R / T)

import chem3
import os
import chem3.parser

class ReactionSystem():
	"""ReactionSystem Class for chemical kinetics calculations

	ATRIBUTES:
	=========
	concs: 		list of floats
				Reactant concentrations
				Must be positive
	nu_react: 	list of floats
	 			Stoichiometric coefficients for reactants
	nu_prod: 	list of floats
				Stoichiometric coefficients for products
	ks:			list of floats
				Reaction rate coefficients

	METHODS:
	=======
	.__init__: init attributes
	.__len__: returns the number of reactions in the system
	.init_matrices: returns reactant and product matrices
	.progress_rate: returns progress rate of system of reactions
	.reaction_rate: returns reaction rate of system of reactions

	EXAMPLES:
	========
	>>> from chem3.parser import read_data
	>>> import os
	>>> test_data_dir = os.path.join(os.path.dirname(chem3.__file__), '../tests/test_data')
	>>> db_name = os.path.join(test_data_dir, 'nasa.sqlite')
	>>> file_name = os.path.join(test_data_dir, 't.xml')
	>>> data = read_data(file_name, db_name)
	>>> concs = [2., 1., .5, 1., 1.]
	>>> T = 1500
	>>> system = ReactionSystem(data['reactions']['test_mechanism'], data['species'])
	>>> print(system.reaction_rate(concs, T))
	[ -2.81117621e+08  -2.85597559e+08   5.66715180e+08   4.47993847e+06
	  -4.47993847e+06]
	"""
	def __init__(self, reactions=[], order=[], nasa7_coeffs_low=[], nasa7_coeffs_high=[], tmid=[], trange=[],\
							 filename=''):
		"""Sets class attributes and returns reference of the class object

		INPUTS
		======
		reactions: 	list of Reaction()
					All reactions in the system
		order:		list of floats
					Species of reactants and products in the system
		T:			float
					Temperature
					Must be positive
		filename:	str
					Name of .xml data file
					Optional field
					If filename is specified, we will use the data
					read from the given file instead of reactions and order

		Assumption
		======
		Current version assumes only one reaction system is read from the
		.xml file, but we might extend this feature to multiple reaction
		systems in the future based on our clients' requirements

		"""
		db_name = os.path.join(os.path.dirname(chem3.__file__), 'nasa.sqlite')

		if filename:
			data = chem3.parser.read_data(filename, db_name)
			reactions = next(iter(data['reactions'].values()))
			order = data['species']
			nasa7_coeffs_low = data['low']
			nasa7_coeffs_high = data['high']
			tmid = data['T_cutoff']
			trange = data['T_range']

		self.order = order
		self.reactions = reactions
		self.nu_react, self.nu_prod = self.init_matrices(reactions)
		self.ks = []

		# Coefficients for reversible reaction
		self.trange = trange
		self.tmid = tmid
		self.p0 = 1.0e+05
		self.R = 8.3144598
		self.nasa7_coeffs_low = nasa7_coeffs_low
		self.nasa7_coeffs_high = nasa7_coeffs_high

	def __len__(self):
		"""Returns the number of reactions in the system"""
		return len(self.reactions)

	def init_matrices(self, reactions):
		"""Initializes reactant and product matrices for progress rate calculations

		INPUTS
		======
		reactions: 	list of Reaction()
					All reactions in the system
		order:		list of floats
					Species of reactants and products in the system

		RETURNS:
		=======
		nu_react: 	array of floats
		 			Stoichiometric coefficients for reactants
		nu_prod: 	array of floats
					Stoichiometric coefficients for products
		"""
		nu_reac = np.zeros((len(self.order), len(reactions)))
		nu_prod = np.zeros((len(self.order), len(reactions)))
		for i in range(len(self.order)):
			for j in range(len(reactions)):
				if self.order[i] in reactions[j].reactants:
					nu_reac[i, j] = reactions[j].reactants[self.order[i]]
				if self.order[i] in reactions[j].products:
					nu_prod[i, j] = reactions[j].products[self.order[i]]
		return nu_reac, nu_prod

	def progress_rate(self, T):
		"""Returns the progress rate of a system of irreversible, elementary reactions

		RETURNS:
		========
		omega: numpy array of floats
			   size: number of reactions
			   progress rate of each reaction
		"""

		# Calcualte forward reaction rate coefficient 
		self.ks = []
		for reac in self.reactions:
			reac.set_reac_coefs(T)
			self.ks.append(reac.k)

		progress = self.ks.copy() # Initialize progress rates with reaction rate coefficients
		for jdx, prog in enumerate(progress):
			if prog < 0:
				raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(prog))

			for idx, xi in enumerate(self.concs):
				nu_ijp = self.nu_react[idx, jdx]
				if xi  < 0.0:
					raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
				if nu_ijp < 0:
					raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ijp))

				progress[jdx] *= xi**nu_ijp

			
			# calculate backward progress rate here 
			back_prog = 0
			if self.reactions[jdx].reversible:
				# cols = []
				# for i in range(len(self.order)):
				# 	if self.order[i] in self.reactions[jdx].reactants:
				# 		cols.append(i)
				back_prog = self.backward_coeffs(self.nu_prod[:, jdx] - self.nu_react[:, jdx], self.ks[jdx], T)

			backward_sub = back_prog
			for idx, xi in enumerate(self.concs):
				nu_ijpp = self.nu_prod[idx, jdx]
				if nu_ijpp < 0:
					raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ijpp))
				backward_sub *= xi**nu_ijpp

			progress[jdx] -= backward_sub

		return progress

	def reaction_rate(self, concs=[], T=0):
		"""Returns the reaction rate of a system of irreversible, elementary reactions

		RETURNS:
		========
		f: numpy array of floats
		   size: number of species
		   reaction rate of each species
		"""
		if len(concs) != len(self.order):
			raise ValueError("Concentration length does not match number of species!")

		if any(c < 0 for c in concs):
			raise ValueError('Concentration should not be Negative!')

		if T <=0:
			raise ValueError('Temperature should be positive!')
			
		self.concs = concs

		rates = self.progress_rate(T)
		nu = self.nu_prod - self.nu_react

		return np.dot(nu, rates)


	def Cp_over_R(self, T):
		"""Helper function that calculates Cp/R

		INPUTS
		======
		T:		Temperature to select nasa coefficient table

		RETURNS:
		=======
		Cp_R: 	Calculated Cp/R
		"""
		a = np.zeros(self.nasa7_coeffs_low.shape)
		for i, tmid in enumerate(self.tmid):
			if T < tmid:
				a[i] = self.nasa7_coeffs_low[i]
			else:
				a[i] = self.nasa7_coeffs_high[i]

		Cp_R = (a[:,0] + a[:,1] * T + a[:,2] * T**2.0 
				+ a[:,3] * T**3.0 + a[:,4] * T**4.0)

		return Cp_R

	def H_over_RT(self, T):
		"""Helper function to calculate H/(RT)

		INPUTS
		======
		T:		Temperature to select nasa coefficient table

		RETURNS:
		=======
		H_RT: 	Calculated H/(RT)
		"""
		a = np.zeros(self.nasa7_coeffs_low.shape)
		for i, tmid in enumerate(self.tmid):
			if T < tmid:
				a[i] = self.nasa7_coeffs_low[i]
			else:
				a[i] = self.nasa7_coeffs_high[i]

		H_RT = (a[:,0] + a[:,1] * T / 2.0 + a[:,2] * T**2.0 / 3.0 
				+ a[:,3] * T**3.0 / 4.0 + a[:,4] * T**4.0 / 5.0 
				+ a[:,5] / T)

		return H_RT
			   

	def S_over_R(self, T):
		"""Helper function to calculate S/R

		INPUTS
		======
		T:		Temperature to select nasa coefficient table

		RETURNS:
		=======
		S_R: 	Calculated S/R
		"""
		a = np.zeros(self.nasa7_coeffs_low.shape)
		for i, tmid in enumerate(self.tmid):
			if T < tmid:
				a[i] = self.nasa7_coeffs_low[i]
			else:
				a[i] = self.nasa7_coeffs_high[i]

		S_R = (a[:,0] * np.log(T) + a[:,1] * T + a[:,2] * T**2.0 / 2.0 
			   + a[:,3] * T**3.0 / 3.0 + a[:,4] * T**4.0 / 4.0 + a[:,6])

		return S_R

	def backward_coeffs(self, nuij, kf, T):
		"""Calculates the backward coefficients: first calculatest the 
			equilibrium coeffients and then calculate backward coefficients

		INPUTS
		======
		nuij:	nuijpp - nuijp -> product nuij - reactant nuij
		kf: 	Forward progress rate of current reaction
		T:		Temperature to select nasa coefficient table

		RETURNS:
		=======
		kf / kb: 	Calculated backward progress rate
		"""

		for i, ran in enumerate(self.trange):
			if T < ran[0] or T > ran[1]:
				raise ValueError("This Temperature is out of range!")

		# Change in enthalpy and entropy for each reaction
		delta_H_over_RT = np.dot(nuij.T, self.H_over_RT(T))
		delta_S_over_R = np.dot(nuij.T, self.S_over_R(T))

		# Negative of change in Gibbs free energy for each reaction 
		delta_G_over_RT = delta_S_over_R - delta_H_over_RT

		# Prefactor in Ke
		fact = self.p0 / self.R / T

		# Ke
		gamma = np.sum(nuij, axis=0)
		kb = fact**gamma * np.exp(delta_G_over_RT)

		return kf / kb



