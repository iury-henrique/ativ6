"""Testes das classes do sistema bancário."""

import unittest

from main import Cliente, Conta, ContaCorrente, ContaPoupanca


class SistemaBancarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cliente = Cliente("  Joana Silva ", "JOANA@example.com")

    def test_cliente_normaliza_nome_e_email(self) -> None:
        self.assertEqual(self.cliente.nome, "Joana Silva")
        self.assertEqual(self.cliente.email, "joana@example.com")

    def test_cliente_rejeita_email_invalido(self) -> None:
        with self.assertRaises(ValueError):
            self.cliente.email = "email-invalido"

    def test_conta_rejeita_saldo_negativo(self) -> None:
        with self.assertRaises(ValueError):
            ContaCorrente(1, self.cliente, -1)

    def test_deposito_e_saque_atualizam_saldo(self) -> None:
        conta = ContaCorrente(1, self.cliente, 100)
        conta.depositar(25)
        conta.sacar(40)
        self.assertEqual(conta.saldo, 85)

    def test_saque_maior_que_saldo_e_rejeitado(self) -> None:
        conta = ContaCorrente(1, self.cliente, 20)
        with self.assertRaises(ValueError):
            conta.sacar(21)

    def test_rendimento_e_polimorfico(self) -> None:
        contas: list[Conta] = [
            ContaCorrente(1, self.cliente, 100),
            ContaPoupanca(2, self.cliente, 100, 0.1),
        ]
        self.assertEqual(
            [conta.calcular_rendimento() for conta in contas],
            [0, 10],
        )

    def test_taxa_de_poupanca_deve_ser_valida(self) -> None:
        with self.assertRaises(ValueError):
            ContaPoupanca(1, self.cliente, 100, 1.1)

    def test_classe_base_e_abstrata(self) -> None:
        with self.assertRaises(TypeError):
            Conta(1, self.cliente)  # type: ignore[abstract]

    def test_contas_comparam_por_tipo_numero_e_saldo(self) -> None:
        primeira = ContaCorrente(1, self.cliente, 100)
        mesma_conta = ContaCorrente(1, self.cliente, 500)
        outra_conta = ContaPoupanca(1, self.cliente, 50)
        self.assertEqual(primeira, mesma_conta)
        self.assertNotEqual(primeira, outra_conta)
        self.assertLess(outra_conta, primeira)


if __name__ == "__main__":
    unittest.main()
