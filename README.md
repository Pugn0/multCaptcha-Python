# Captcha Solver

Este projeto é uma ferramenta para resolver captchas de forma automatizada em páginas da web, utilizando serviços como **CapMonster** e **2Captcha**.

## Requisitos

- **Python 3.12.8** (Versão utilizada neste projeto)
- Conexão com um dos serviços suportados (CapMonster ou 2Captcha)

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-repositorio/captcha-solver.git
   cd captcha-solver
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

## Como Usar

1. **Execute o script principal:**
   ```sh
   python solver.py
   ```

2. **Escolha o tipo de captcha que deseja resolver.**

3. **Insira as informações necessárias**, como chaves de API e URLs das páginas da web.

4. **Aguarde a conclusão do processo**. O resultado da resolução do captcha será exibido na tela.

## Opções Disponíveis

- ✅ CapMonster [reCaptcha V2]
- ✅ CapMonster [reCaptcha V3]
- ✅ CapMonster [hCaptcha]
- ✅ CapMonster [Captcha de Texto]
- ✅ 2Captcha [reCaptcha V2]
- ✅ 2Captcha [reCaptcha V3]
- ✅ 2Captcha [hCaptcha]

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir **issues** ou enviar **pull requests** com melhorias ou correções de bugs.

## Licença

Este projeto está sob a [Licença MIT](LICENSE).

