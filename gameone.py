class Person:
  nome = ""  #nome del personaggio
  soldi = 0  #soldi che il personaggio ha
  amici = []  #lista degli amici
  Bc = 0  #BIGGY coins
  level = 0  #livello giocatore
  exp = 0
  pfp = ""  #immagine profilo del giocatore
  description = ""  #descrizione del giocatore

  #nel caso in cui non si passi alcun valore allora viene inizializzato a 0
  def __init__(self) -> None:
    pass

  #metodo con i valori che vengono passati
  def __init__(self, name, money, amici, biggyCoins, livello, exp, pfp,
               description):
    self.name = name
    self.soldi = money
    self.amici = amici
    self.Bc = biggyCoins
    self.level = livello
    self.exp = exp
    self.pfp = pfp
    self.description = description

  #

#region get/set del nome

  def getName(self):
    return self.nome

  def setName(self, name):
    self.nome = name
#endregion

#region get/set dei soldi

  def getSoldi(self):
    return self.soldi

  def setSoldi(self, coins):
    self.soldi = coins
#endregion

#region get/set/add/remove degli amici

  def getAmici(self, ):
    return self.amici.size()

  def addAmici(self, person):
    self.amici.append(person)

  def removeAmici(self, person):
    self.amici.remove(person)
#endregion

#region get/add BIGGYCOINS

  def getBiggyCoins(self):
    return self.Bc

  def addBiggyCoins(self, amount):
    self.Bc += amount
#endregion

#region get level

  def getLevel(self):
    return self.level
#endregion

#region get/add EXP

  def getExp(self):
    return self.exp

  def addExp(self, sium):
    self.exp += sium
#endregion

#region get/set profile picture

  def getPfp(self):
    return self.pfp

  def setPfp(self, pp):
    self.pfp = pp
#endregion

#region get/set Descrizione

  def getDescription(self):
    return self.description

  def setDescription(self, dsc):
    self.description = dsc


#endregion