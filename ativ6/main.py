"""Exemplo de modelagem orientada a objetos para um sistema bancário."""

from abc import ABC, abstractmethod
import re
from math import isfinite


def _validar_valor_monetario(valor: float, nome: str) -> float:
    """Retorna um valor numérico finito ou informa que ele é inválido."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"{nome} deve ser um número.")
    if not isfinite(valor):
        raise ValueError(f"{nome} deve ser finito.")
    return float(valor)


class Cliente:
    """Representa uma pessoa titular de uma ou mais contas."""

    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email

    @property
    def nome(self) -> str:
        """Nome do cliente."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        """Atualiza o nome após validar que não está vazio."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome deve ser um texto não vazio.")
        self._nome = valor.strip()

    @property
    def email(self) -> str:
        """Endereço de e-mail validado do cliente."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Atualiza o e-mail após validar seu formato básico."""
        if not isinstance(valor, str):
            raise TypeError("O e-mail deve ser um texto.")
        email = valor.strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError("O e-mail informado não é válido.")
        self._email = email.lower()

    def __str__(self) -> str:
        """Retorna os dados do cliente em formato legível."""
        return f"{self.nome} ({self.email})"

    def __repr__(self) -> str:
        """Retorna uma representação útil para depuração."""
        return f"{type(self).__name__}(nome={self.nome!r}, email={self.email!r})"


class Conta(ABC):
    """Classe base abstrata para contas bancárias."""

    def __init__(self, numero: int, titular: Cliente, saldo: float = 0) -> None:
        self.numero = numero
        self.titular = titular
        self.saldo = saldo

    @property
    def numero(self) -> int:
        """Número identificador da conta."""
        return self._numero

    @numero.setter
    def numero(self, valor: int) -> None:
        """Atualiza o número somente quando ele é um inteiro positivo."""
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValueError("O número da conta deve ser um inteiro positivo.")
        self._numero = valor

    @property
    def titular(self) -> Cliente:
        """Cliente associado à conta."""
        return self._titular

    @titular.setter
    def titular(self, valor: Cliente) -> None:
        """Associa à conta somente um cliente válido."""
        if not isinstance(valor, Cliente):
            raise TypeError("O titular deve ser uma instância de Cliente.")
        self._titular = valor

    @property
    def saldo(self) -> float:
        """Saldo atual, que não pode ser negativo."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        """Atualiza o saldo somente com um valor finito e não negativo."""
        saldo = _validar_valor_monetario(valor, "O saldo")
        if saldo < 0:
            raise ValueError("O saldo não pode ser negativo.")
        self._saldo = saldo

    def depositar(self, valor: float) -> None:
        """Adiciona um valor positivo ao saldo."""
        valor_validado = _validar_valor_monetario(valor, "O depósito")
        if valor_validado <= 0:
            raise ValueError("O depósito deve ser maior que zero.")
        self.saldo += valor_validado

    def sacar(self, valor: float) -> None:
        """Retira um valor positivo que não ultrapasse o saldo."""
        valor_validado = _validar_valor_monetario(valor, "O saque")
        if valor_validado <= 0:
            raise ValueError("O saque deve ser maior que zero.")
        if valor_validado > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor_validado

    @abstractmethod
    def calcular_rendimento(self) -> float:
        """Calcula o rendimento da conta sem alterar seu saldo."""

    def __str__(self) -> str:
        """Retorna os dados comuns da conta em formato legível."""
        return (
            f"{type(self).__name__} nº {self.numero} | "
            f"Titular: {self.titular.nome} | Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self) -> str:
        """Retorna uma representação da conta útil para depuração."""
        return (
            f"{type(self).__name__}(numero={self.numero!r}, "
            f"titular={self.titular!r}, saldo={self.saldo!r})"
        )

    def __eq__(self, outro: object) -> bool:
        """Compara contas pelo tipo concreto e pelo número."""
        if not isinstance(outro, Conta):
            return NotImplemented
        return type(self) is type(outro) and self.numero == outro.numero

    def __lt__(self, outro: object) -> bool:
        """Ordena contas pelo saldo."""
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.saldo < outro.saldo


class ContaCorrente(Conta):
    """Conta sem rendimento, sujeita a uma tarifa mensal."""

    def __init__(
        self,
        numero: int,
        titular: Cliente,
        saldo: float = 0,
        tarifa_mensal: float = 0,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self.tarifa_mensal = tarifa_mensal

    @property
    def tarifa_mensal(self) -> float:
        """Tarifa mensal não negativa da conta."""
        return self._tarifa_mensal

    @tarifa_mensal.setter
    def tarifa_mensal(self, valor: float) -> None:
        """Atualiza a tarifa somente com um valor finito não negativo."""
        tarifa = _validar_valor_monetario(valor, "A tarifa mensal")
        if tarifa < 0:
            raise ValueError("A tarifa mensal não pode ser negativa.")
        self._tarifa_mensal = tarifa

    def calcular_rendimento(self) -> float:
        """Conta corrente não gera rendimento."""
        return 0.0

    def __str__(self) -> str:
        """Inclui a tarifa na representação legível da conta corrente."""
        return f"{super().__str__()} | Tarifa: R$ {self.tarifa_mensal:.2f}"


class ContaPoupanca(Conta):
    """Conta cujo rendimento é calculado por uma taxa percentual."""

    def __init__(
        self,
        numero: int,
        titular: Cliente,
        saldo: float = 0,
        taxa_rendimento: float = 0.005,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self) -> float:
        """Taxa de rendimento entre zero e um, inclusive."""
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor: float) -> None:
        """Atualiza a taxa somente quando está entre zero e um."""
        taxa = _validar_valor_monetario(valor, "A taxa de rendimento")
        if not 0 <= taxa <= 1:
            raise ValueError("A taxa de rendimento deve estar entre 0 e 1.")
        self._taxa_rendimento = taxa

    def calcular_rendimento(self) -> float:
        """Calcula o rendimento do saldo conforme a taxa da poupança."""
        return self.saldo * self.taxa_rendimento

    def __str__(self) -> str:
        """Inclui a taxa na representação legível da conta poupança."""
        return (
            f"{super().__str__()} | "
            f"Rendimento: {self.taxa_rendimento:.2%}"
        )


def demonstrar_sistema() -> None:
    """Cria objetos de exemplo, demonstra polimorfismo e validações."""
    clientes = [
        Cliente("Ana Silva", "ana@example.com"),
        Cliente("Bruno Souza", "bruno@example.com"),
        Cliente("Carla Lima", "carla@example.com"),
        Cliente("Diego Alves", "diego@example.com"),
        Cliente("Eva Costa", "eva@example.com"),
    ]
    contas: list[Conta] = [
        ContaCorrente(1001, clientes[0], 1200, 12.50),
        ContaPoupanca(1002, clientes[0], 2500, 0.01),
        ContaCorrente(1003, clientes[1], 800),
        ContaPoupanca(1004, clientes[1], 1500, 0.008),
        ContaCorrente(1005, clientes[2], 320),
        ContaPoupanca(1006, clientes[2], 4000, 0.012),
        ContaCorrente(1007, clientes[3], 2100, 8),
        ContaPoupanca(1008, clientes[3], 900, 0.006),
        ContaCorrente(1009, clientes[4], 675),
        ContaPoupanca(1010, clientes[4], 1800, 0.01),
    ]

    print("Contas e rendimentos (polimorfismo):")
    for conta in contas:
        print(f"{conta} | Rendimento calculado: R$ {conta.calcular_rendimento():.2f}")

    print("\nRepresentações:")
    print(repr(contas[0]))

    print("\nExemplos de entradas inválidas:")
    for descricao, acao in (
        ("e-mail", lambda: Cliente("Pessoa", "email-invalido")),
        ("saldo", lambda: ContaCorrente(2001, clientes[0], -10)),
        ("saque", lambda: contas[0].sacar(100_000)),
    ):
        try:
            acao()
        except (TypeError, ValueError) as erro:
            print(f"{descricao.capitalize()} rejeitado: {erro}")


if __name__ == "__main__":
    demonstrar_sistema()
