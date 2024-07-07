from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas_cliente = []
    
    def fazer_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def add_conta(self, conta):
        self.contas_cliente.append(conta)

class pessoafisica(cliente):
    def __init__(self, nome, data, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data = data
        self.cpf = cpf

class conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.cliente = cliente
        self.agencia = "0001"
        self.historico = historico()

    @classmethod
    def conta_criada(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def numero(self):
        return self.numero
    @property
    def cliente(self):
        return self.cliente
    @property
    def agencia(self):
        return self.agencia
    @property
    def saldo(self):
        return self.saldo
    @property
    def historico(self):
        return self.historico
    
    def sacar_dinheiro(self, valor):
        saldo = self.saldo
        saldo_excedido = saldo < valor
        if saldo_excedido:
            print("\nA Operação falhou! Saldo insuficiente.")
        elif valor > 0:
            self.saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nA operação não pôde ser realizada. O valor informado é inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("\nDepósito fetocom sucesso!")
        else:
            print("\nA Operação falhou! O valor informado é inválido")
            return False
        return True
    
class contacorrente(conta):
    def __init__(self, cliente, numero, limite=500, limite_saque=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        qtd_saques = len([transacao for transacao in self.historico.transacao if transacao["Tipo"] == Saque.__name__])

        limite_excedido = valor > self.limite
        saque_excedido = qtd_saques >= self.limite_saque

        if limite_excedido:
            print("\nA operação falhou! O valor do saque está excedendo seu limite.")
        elif saque_excedido:
            print("\nA operação falhou! O limite de saques foi excedido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            CC:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class historico:
    def __init__(self):
        self.transacoes = []
    
    @property
    def transacoes(self):
        return self.transacoes
    
    def add_transacao(self, transacao):
        self.transacoes.append({"tipo": transacao.__class__.__name__,
                                "valor": transacao.valor,})
        
class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class saque(transacao):
    def __init__(self, valor):
        self.valor = valor
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.add_transacao(self)

class deposito(transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.add_transacao(self)
