# IAM Operations

## Descrição do Projeto
Esse projeto tem como objetivo facilitar o gerenciamento de usuários em sua conta AWS. O script utiliza o SDK da AWS para Python3 (Boto3), realizando suas ações através do IAM.

##  Funcionalidades do Script
* [Listar todos os usuários da conta e suas Access Keys](#listar-todos-os-usuários-da-conta-e-suas-access-keys)
* [Listar todos os usuários que não utilizem as Access Keys a mais de X dias](#listar-todos-os-usuários-que-não-utilizem-as-access-keys-a-mais-de-x-dias)

## Listar todos os usuários da conta e suas Access Keys
Nessa função, o script lista todos os usuários e também todas as suas Access Keys. Esse é modo padrão de execução, caso não seja passado nenhum argumento, o script irá trazer todos os usuários.

Alguns exemplos de utilização:
```
python3 iam_operations.py
python3 iam_operations.py all
python3 iam_operations.py all ./users.json
```
A saída será um arquivo JSON, com a seguinte sintaxe:
```
{
   "Date": "2022-04-04 12:34:19.619317",
   "Users": [
      {
         "UserName": "user_name_access_key_used",
         "PasswordLastUsed": "01/01/2022",
         "AccessKeys": [
            {
               "AccessKeyId": "access_key_id",
               "Status": "Active",
               "CreateDate": "01/01/2022",
               "LastUsed": "01/01/2022"
            }
         ]
      },
      {
         "UserName": "user_name_no_access_key",
         "PasswordLastUsed": "N/A",
         "AccessKeys": []
      },
      {
         "UserName": "user_name_access_key_never_used",
         "PasswordLastUsed": "N/A",
         "AccessKeys": [
            {
               "AccessKeyId": "access_key_id",
               "Status": "Active",
               "CreateDate": "01/01/2022",
               "LastUsed": "N/A"
            }
         ]
      }
   ]
}
```
Ver também: [Modos de utilização](#modos-de-utilização)

## Listar todos os usuários que não utilizem as Access Keys a mais de X dias.
Nessa função, o script lista todos os usuários que não utilizaram uma ou mais Access Keys em um período de tempo de X dias (90 dias por padrão).

Alguns exemplos de utilização:
```
python3 iam_operations.py validateKeys
python3 iam_operations.py validateKeys ./users.json
```
A saída será um arquivo JSON, seguindo a mesma sintaxe da função [Listar todos os usuários da conta e suas Access Keys](#listar-todos-os-usuários-da-conta-e-suas-access-keys)

Ver também: [Modos de utilização](#modos-de-utilização)

## Modos de utilização
Um dos casos de uso pensados para esse script foi ser utilizados em esteiras de automação. Por exemplo: Executar o script no início de cada mês, gerando um JSON para verificar usuários com Access Keys que não estão sendo utilizadas, que será usado em uma função de notificação, enviando um Email aos usuários para inativarem suas chaves, diminuindo assim portas de entrada para possíveis invasores.

Uma das preocupações foi deixar a saída para ser trabalhada como preferir, você pode simplesmente utiliza-lo em uma pipeline para exibir esses usuários, ou guardar o JSON para ser utilizado em outras funções. Por isso, foi pensado um sistema de parâmetros para facilitar o uso.
Os parâmetros possíveis são:

```
python3 iam_operations.py <modo_execução> <caminho_arquivo_final>
```

No primeiro parâmetro é passado o modo de execução. Os modos possíveis são:
- all - Ver: [Listar todos os usuários da conta e suas Access Keys](#listar-todos-os-usuários-da-conta-e-suas-access-keys);
- validateKeys - Ver: [Listar todos os usuários que não utilizem as Access Keys a mais de X dias](#listar-todos-os-usuários-que-não-utilizem-as-access-keys-a-mais-de-x-dias);

O modo "all" é padrão, caso a intenção for usar o modo all e não salvar a saída em nenhum arquivo, não é necessário passar nenhum parâmetro. Caso necessário utilizar o parâmetro de arquivo externo, o primeiro parâmetro se torna obrigatório.

No segundo parâmetro, é passado o caminho do arquivo onde o JSON final vai ser salvo. Esse parâmetro não é obrigatório, caso não seja utilizado, o script não salvará o JSON em um arquivo e irá apenas exibi-ló. Caso utilizado, o JSON não é exibido, apenas salvo em um arquivo.

## Variáveis de Ambiente
O script necessita das credências de um usuário AWS. É recomendado criar um usuário com permissões relacionadas ao IAM apenas.

Caso você ja tenha um perfil configurado pelo AWS CLI, você pode exportar a variável **AWS_PROFILE**, para que o script utiliza as credenciais do perfil.

Também é possível exportar as credenciais diretamente por variáveis, um cenário mais viável quando se utilize ferramentar para automação, para isso, é necessário exportar as seguintes variáveis:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_SESSION_TOKEN (caso o usuário tenha MFA habilitado.)