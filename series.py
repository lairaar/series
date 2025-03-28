import pickle
import os

def limparTela():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")


class Serie:
	def __init__(self, cod, nome):
		self.cod = cod
		self.nome = nome
		self.temporadas = []
	
	def __str__(self):
		return self.nome


class Temporada:
	def __init__(self, num, ano):
		self.num = num
		self.ano = ano
		self.episodios = []

	def __str__(self):
		return "Temporada {}".format(self.num)


class Episodio:
	def __init__(self, num, nome):
		self.num = num
		self.nome = nome # nome esta armazenando o titulo do episodio

	def __str__(self):
		return "Episódio {} ({})".format(self.num, self.nome)


class EpAssistido:
	def __init__(self, serie, temporada, episodio):
		self.serie = serie
		self.temporada = temporada
		self.episodio = episodio
	
	def __str__(self):
		return "{} S{}E{}".format(self.serie.nome, self.temporada.num, self.episodio.num)
	
	def equals(self, codSerie, numT, numEp):
		if self.serie.cod == codSerie and self.temporada.num == numT and self.episodio.num == numEp:
			cont += 1
			return cont 

class Usuario:
	def __init__(self, nome, login, senha):
		self.nome = nome
		self.login = login
		self.senha = senha
		self.favoritas = []
		self.assistidos = []
	
	def __str__(self):
		return self.nome
	
	def seguindo(self, cod):
		for serie in self.favoritas:
			if serie.cod == cod: return True
		
		return False

	def verificarEpisodioAssistido(self, codSerie, numT, numEp):
		for epAssistido in self.assistidos:
			if epAssistido.equals(codSerie, numT, numEp): return True
		
		return False

class Sistema:
	def __init__(self):
		self.series = []
		self.usuarios = []
	
	def carregarDados(self, arquivo):
		''' Dados iniciais carregados automaticamente. Não alterar. '''
		if os.path.isfile(arquivo):
			with open(arquivo, "rb") as arq:
				self.series = pickle.load(arq)
				self.usuarios = pickle.load(arq)

	def buscarUsuario(self, login):
		for usuario in self.usuarios:
			if login == usuario.login: return usuario
		
		return None
		
	def buscarSerie(self, cod):
		for serie in self.series:
			if cod == serie.cod: return serie
		
		return None
		
	def autenticar(self, login, senha):
		usuario = self.buscarUsuario(login)
		if usuario is not None:
			if usuario.senha == senha: return True
			else: 
				print("Senha inválida.")
				return False
		else:
			print("Usuário inexistente.")
			return False
	
	def bemVindo(self, login):
		usuario = self.buscarUsuario(login)
		print("\nBem-vindo, {}!\n".format(usuario))

	def exibirSeries(self, login):
		usuario = self.buscarUsuario(login)
		for fav in usuario.favoritas:
			print(fav)
	
	def exibirEpisodiosAtrasados(self, login):
		usuario = self.buscarUsuario(login)
		for fav in usuario.favoritas:
			for t in fav.temporadas:
				for ep in t.episodios:
					if not usuario.verificarEpisodioAssistido(fav.cod, t.num, ep.num):
						print(ep)

		
	def estatisticas(self, login):
		contAtraso = 0
		contAssistido = 0
		contFav = 0
		usuario = self.buscarUsuario(login)
		for fav in usuario.favoritas:
			for t in fav.temporadas:
				for ep in t.episodios:
					if not usuario.verificarEpisodioAssistido(fav.cod, t.num, ep.num):
						contAtraso += 1
					else:
						contAssistido += 1
		for serie in usuario.favoritas:
			contFav += 1
		print()
		print("Quantidade de episodios atrasados: ", contAtraso)
		print("Quantidade de episodios assistidos: ", contAssistido)
		print("Quantidade de episodios favoritos: ", contFav)
		print()
		
	def marcarEpisodio(self, login):
		usuario = self.buscarUsuario(login)
		print("Séries favoritas")
		for fav in usuario.favoritas:
			print(fav.cod, fav.nome)
			serieCod = input("Digite o codigo da serie desejada: ")
			if serieCod == fav.cod:
				serie = fav
				for t in fav.temporada:
					print(t)
					numTemp = int(input("Digite o número da temporada: "))
					if t.num == numTemp:
						temporada = t
						for ep in t.episodios:
							print(ep)
							numEp = int(input("Digite o número de episódeos: "))
							if ep.num == numEp:
								episodio = ep
		assistido = EpAssistido(serie, temporada, episodio)
		usuario.assistidos.append(assistido)


 
def main(argv=None):
	menu = '''
Escolha uma opção:
1 - Visualizar séries favoritas
2 - Visualizar episódios atrasados
3 - Visualizar estatísticas
4 - Marcar episódio como assistido
0 - Sair
'''

	s = Sistema()
	s.carregarDados("series.bin")

	for serie in s.series:
		print(serie.cod)
		for t in serie.temporadas:
			print(t)
			for p in t.episodios:
				print(p) 
	
	
	login = input("login: ")
	senha = input("senha: ")
	
	if s.autenticar(login, senha):
		s.bemVindo(login)
		print(menu)
		opt = input()

		while opt != '0':
			limparTela()
			if opt == '1':
				print("Escolhi a opção 1")
				s.exibirSeries(login)
			elif opt == '2':
				print("Escolhi a opção 2")
				s.exibirEpisodiosAtrasados(login)
			elif opt == '3':
				print("Escolhi a opção 3")
				s.estatisticas(login)
			elif opt == '4':
				print("Escolhi a opção 4")
				s.marcarEpisodio(login)
			else:
				print("Opção inválida.")
		
			print(menu)
			opt = input()
	
		print("Até a próxima!")


if __name__ == '__main__':
	main()

