import json,re
from pathlib import Path
# Each recipe specifies a different rule or algorithm. Loop structures deliberately
# revisit these algorithms with their own traversal mechanics and input datasets.
decisions=[
('Entrada para o cinema','idade',18,'idade >= 16','a idade é pelo menos 16 anos','>= 16'),
('Sensor de congelamento','temperatura',-3,'temperatura < 0','a temperatura é negativa','< 0'),
('Número par','numero',24,'numero % 2 === 0','o número é par','% 2 === 0'),
('Estoque esgotado','estoque',0,'estoque === 0','o estoque está zerado','=== 0'),
('Frete por valor','total',230,'total >= 200','a compra alcança 200 reais','>= 200'),
('Senha com tamanho mínimo','senha','segredo123','senha.length >= 8','a senha tem pelo menos oito caracteres','.length >= 8'),
('Múltiplo de cinco','numero',35,'numero % 5 === 0','o número é múltiplo de cinco','% 5 === 0'),
('Domínio de e-mail','email','ana@exemplo.com','email.endsWith("@exemplo.com")','o e-mail termina em @exemplo.com','endsWith'),
('Modo de manutenção','manutencao',True,'manutencao === true','a manutenção está ativa','=== true'),
('Nome vazio','nome','','nome.length === 0','o nome está vazio','.length === 0'),
('Arquivo JavaScript','arquivo','index.js','arquivo.endsWith(".js")','o arquivo tem extensão .js','endsWith'),
('Palavra inicial','mensagem','Olá, mundo','mensagem.startsWith("Olá")','a mensagem começa com Olá','startsWith'),
('Limite de velocidade','velocidade',95,'velocidade > 80','a velocidade ultrapassa 80','> 80'),
('Saldo negativo','saldo',-12,'saldo < 0','o saldo é negativo','< 0'),
('Cupom exato','cupom','NODE10','cupom === "NODE10"','o cupom corresponde exatamente a NODE10','=== "NODE10"'),
('Fila vazia','fila',[],'fila.length === 0','a fila está vazia','.length === 0'),
('Letra encontrada','palavra','javascript','palavra.includes("a")','a palavra contém a letra a','includes'),
('Raiz inteira','numero',49,'Number.isInteger(Math.sqrt(numero))','a raiz quadrada é inteira','isInteger'),
('Divisibilidade por três','numero',27,'numero % 3 === 0','o número é divisível por três','% 3 === 0'),
('Identificador positivo','id',12,'id > 0','o identificador é positivo','> 0'),
('Valor ausente','valor',None,'valor === null','o valor é null','=== null'),
('Tipo textual','dado','Node','typeof dado === "string"','o dado é uma string','typeof'),
('Temperatura de fervura','temperatura',100,'temperatura >= 100','a temperatura alcança 100 graus','>= 100'),
('Desconto por quantidade','quantidade',12,'quantidade >= 10','há pelo menos dez unidades','>= 10'),
('Sinal de exclamação','texto','Atenção!','texto.endsWith("!")','o texto termina com exclamação','endsWith'),
('Comprimento exato','codigo','ABC123','codigo.length === 6','o código tem seis caracteres','.length === 6'),
('Preço dentro do orçamento','preco',40,'preco <= 50','o preço não supera 50 reais','<= 50'),
('Primeiro elemento','valores',[7,2,8],'valores[0] === 7','o primeiro elemento é sete','[0] === 7'),
('Número inteiro','numero',4.5,'Number.isInteger(numero)','o número é inteiro','isInteger'),
('Texto sem conteúdo','texto','   ','texto.trim().length === 0','o texto contém apenas espaços ou está vazio','trim'),
]
medium=[
('Faixa de trabalho','hora',14,'hora >= 9 && hora < 18','a hora está entre 9 (inclusive) e 18 (exclusive)'),
('Acesso com assinatura','pessoa',{'ativa':True,'bloqueada':False},'pessoa.ativa && !pessoa.bloqueada','a assinatura está ativa e não bloqueada'),
('Entrega expressa','pedido',{'peso':4,'distancia':18},'pedido.peso <= 5 && pedido.distancia <= 20','peso até 5 kg e distância até 20 km'),
('Ano com final zero','ano',2030,'ano % 10 === 0 && ano % 100 !== 0','o ano termina em zero, mas não em 00'),
('Elegibilidade para bolsa','aluno',{'nota':8.5,'renda':1500},'aluno.nota >= 8 && aluno.renda <= 2000','nota mínima oito e renda de até 2000'),
('Intervalo fora da faixa','valor',120,'valor < 0 || valor > 100','o valor está fora de 0 a 100'),
('Triângulo possível','lados',[4,5,7],'lados[0] + lados[1] > lados[2] && lados[0] + lados[2] > lados[1] && lados[1] + lados[2] > lados[0]','cada lado é menor que a soma dos outros dois'),
('Senha sem espaços','senha','forte1234','senha.length >= 8 && !senha.includes(" ")','há oito caracteres ou mais, sem espaços'),
('Fim de semana','dia',6,'dia === 0 || dia === 6','o dia é domingo (0) ou sábado (6)'),
('Cupom normalizado','cupom',' node10 ','cupom.trim().toUpperCase() === "NODE10"','o cupom é NODE10 após retirar espaços externos e ignorar caixa'),
('Metade superior','ponto',{'x':3,'y':8},'ponto.x >= 0 && ponto.y > 0','x não é negativo e y é positivo'),
('Dois valores iguais','valores',[5,5,9],'valores[0] === valores[1] && valores[1] !== valores[2]','os dois primeiros valores são iguais e o terceiro é diferente'),
('Saldo após compra','conta',{'saldo':150,'compra':130},'conta.saldo - conta.compra >= 20','restam pelo menos 20 reais após a compra'),
('Prefixo e sufixo','arquivo','test-user.js','arquivo.startsWith("test-") && arquivo.endsWith(".js")','o nome começa com test- e termina com .js'),
('Divisível por dois e três','numero',42,'numero % 2 === 0 && numero % 3 === 0','o número é divisível por dois e por três'),
('Desconto exclusivo','flags',{'vip':True,'cupom':False},'flags.vip !== flags.cupom','exatamente uma das duas condições é verdadeira'),
('Array com conteúdo','dados',[1,2],'Array.isArray(dados) && dados.length > 0','o dado é um array não vazio'),
('Intervalos sobrepostos','faixas',[2,8,6,10],'faixas[0] <= faixas[3] && faixas[2] <= faixas[1]','dois intervalos fechados possuem interseção'),
('Proximidade numérica','valores',[10,10.04],'Math.abs(valores[0] - valores[1]) <= 0.05','a distância entre os valores é no máximo 0.05'),
('Aprovação com presença','aluno',{'nota':7,'presenca':80},'aluno.nota >= 6 && aluno.presenca >= 75','a nota é no mínimo seis e a presença ao menos 75%'),
('Acesso por função','papel','editor','papel === "admin" || papel === "editor"','o papel é admin ou editor'),
('Paridade diferente','numeros',[4,7],'numeros[0] % 2 !== numeros[1] % 2','os dois números positivos têm paridades diferentes'),
('Texto palíndromo','texto','radar','texto === texto.split("").reverse().join("")','o texto é igual ao seu reverso'),
('Sufixo numérico','texto','pedido42','/\d$/.test(texto)','o texto termina em um dígito'),
('Último item válido','itens',[3,8,11],'itens.length > 0 && itens[itens.length - 1] > 10','o array é não vazio e seu último item supera dez'),
('Temperatura confortável','ambiente',{'temp':23,'umidade':50},'ambiente.temp >= 20 && ambiente.temp <= 26 && ambiente.umidade < 70','temperatura de 20 a 26 e umidade abaixo de 70'),
('Token disponível','token','abc','typeof token === "string" && token.trim().length > 0','o token é string e não está em branco'),
('Potência de dois','numero',32,'numero > 0 && (numero & (numero - 1)) === 0','o inteiro positivo é uma potência de dois'),
('Compra com cashback','pedido',{'total':250,'categoria':'livros'},'pedido.total >= 200 && pedido.categoria === "livros"','a compra de livros é de pelo menos 200 reais'),
('Permissão de edição','registro',{'autor':7,'usuario':7,'fechado':False},'registro.autor === registro.usuario && !registro.fechado','o usuário é autor e o registro não está fechado'),
]
hard=[
('Ano bissexto','ano',2000,'ano % 400 === 0 || (ano % 4 === 0 && ano % 100 !== 0)','o ano é bissexto no calendário gregoriano'),
('Validação de versão','versao','2.14.0','/^\d+\.\d+\.\d+$/.test(versao)','a versão contém exatamente três grupos de dígitos separados por pontos'),
('Número seguro','valor',9007199254740991,'Number.isSafeInteger(valor) && valor > 0','o número é um inteiro positivo seguro'),
('Intervalo circular','horario',{'hora':2,'inicio':22,'fim':6},'horario.inicio <= horario.fim ? horario.hora >= horario.inicio && horario.hora < horario.fim : horario.hora >= horario.inicio || horario.hora < horario.fim','a hora pertence ao intervalo, inclusive quando cruza meia-noite'),
('Estoque com reserva','item',{'total':12,'reserva':5,'pedido':7},'item.pedido > 0 && item.total - item.reserva >= item.pedido','o pedido é positivo e cabe no estoque não reservado'),
('Permissões por bits','mascara',13,'(mascara & 5) === 5','os bits de leitura (1) e execução (4) estão ativos'),
('Parênteses exteriores','texto','(node)','texto.length >= 2 && texto[0] === "(" && texto[texto.length - 1] === ")"','há pelo menos dois caracteres, com ( no começo e ) no fim'),
('Fração equivalente','fracoes',[2,3,8,12],'fracoes[1] !== 0 && fracoes[3] !== 0 && fracoes[0] * fracoes[3] === fracoes[2] * fracoes[1]','as frações são equivalentes e têm denominadores não nulos'),
('Ponto no anel','ponto',{'x':3,'y':4},'ponto.x ** 2 + ponto.y ** 2 >= 9 && ponto.x ** 2 + ponto.y ** 2 <= 36','o ponto está entre raios três e seis, incluindo as bordas'),
('Ordenação estrita','valores',[2,6,9],'valores[0] < valores[1] && valores[1] < valores[2]','três valores estão em ordem estritamente crescente'),
('Checksum decimal','codigo',[4,7,1],'(codigo[0] + codigo[1]) % 10 === codigo[2]','o último dígito é a soma dos dois primeiros módulo dez'),
('Aprovação com exceção','caso',{'nota':5,'recurso':True,'faltas':2},'(caso.nota >= 7 || (caso.nota >= 5 && caso.recurso)) && caso.faltas <= 3','nota sete, ou nota cinco com recurso; no máximo três faltas em ambos os casos'),
('Validade de data ISO','data','2024-02-29','/^\d{4}-\d{2}-\d{2}$/.test(data) && !Number.isNaN(Date.parse(data)) && new Date(data).toISOString().slice(0, 10) === data','a data existe e está no formato AAAA-MM-DD'),
('Chave própria','objeto',{'nome':'Ana'},'Object.hasOwn(objeto, "nome")','nome pertence ao objeto, sem depender da cadeia de protótipos'),
('Regra de roteamento','req',{'metodo':'POST','autorizado':True,'tamanho':512},'req.metodo === "POST" && req.autorizado && req.tamanho > 0 && req.tamanho <= 1024','é POST autorizado, com corpo de 1 a 1024 bytes'),
('Discriminante real','coef',{'a':1,'b':5,'c':6},'coef.a !== 0 && coef.b ** 2 - 4 * coef.a * coef.c >= 0','a equação é quadrática e possui raízes reais'),
('Retângulos em contato','r',[0,0,4,4,3,3,6,6],'r[0] <= r[6] && r[2] >= r[4] && r[1] <= r[7] && r[3] >= r[5]','retângulos definidos por xmin, ymin, xmax, ymax se tocam ou sobrepõem'),
('Escalonamento por prioridade','tarefa',{'urgente':False,'espera':35,'bloqueada':False},'!tarefa.bloqueada && (tarefa.urgente || tarefa.espera >= 30)','a tarefa não está bloqueada e é urgente ou espera ao menos 30 minutos'),
('Hexadecimal curto','cor','#a3F','/^#[0-9a-fA-F]{3}$/.test(cor)','a cor tem # e exatamente três dígitos hexadecimais'),
('IPv4 simplificado','octetos',[192,168,0,1],'octetos.length === 4 && octetos.every(x => Number.isInteger(x) && x >= 0 && x <= 255)','há quatro octetos inteiros entre zero e 255'),
('Limite com tolerância','medida',{'real':100.01,'alvo':100},'Math.abs(medida.real - medida.alvo) <= Math.abs(medida.alvo) * 0.001','o erro absoluto é até 0.1% do valor alvo'),
('Vogais únicas','texto','aeiou','new Set(texto).size === 5 && [...texto].every(c => "aeiou".includes(c))','as cinco vogais minúsculas estão presentes, sem outras letras'),
('Agendamento sem conflito','agenda',{'inicio':10,'fim':12,'ocupadoInicio':12,'ocupadoFim':14},'agenda.inicio < agenda.fim && (agenda.fim <= agenda.ocupadoInicio || agenda.inicio >= agenda.ocupadoFim)','o intervalo é válido e não sobrepõe o ocupado; tocar a borda é permitido'),
('Nome de variável ASCII','nome','_total2','/^[A-Za-z_$][A-Za-z0-9_$]*$/.test(nome)','o identificador começa por letra, _ ou $, seguido apenas por esses caracteres ou dígitos; ignore palavras reservadas'),
('Mês com 31 dias','mes',7,'Number.isInteger(mes) && [1,3,5,7,8,10,12].includes(mes)','o mês é um dos meses de 31 dias'),
('Valor finito não textual','valor',12.5,'typeof valor === "number" && Number.isFinite(valor)','o valor é número finito, sem converter strings'),
('Pedido idempotente','req',{'chave':'abc','processado':False,'tentativas':2},'typeof req.chave === "string" && req.chave.length > 0 && !req.processado && req.tentativas < 3','há chave textual não vazia, pedido ainda não processado e menos de três tentativas'),
('Paridade de bits','numero',11,'numero.toString(2).split("1").length % 2 === 1','a quantidade de bits 1 é par no inteiro não negativo'),
('Segmento degenerado','pontos',[2,3,2,3],'pontos[0] === pontos[2] && pontos[1] === pontos[3]','o início e o fim do segmento são o mesmo ponto'),
('Conjunto contido','grupos',{'a':[1,2],'b':[1,2,3]},'grupos.a.every(x => grupos.b.includes(x))','todo elemento de a pertence a b'),
]
# Loops: title, input, initialization, body, output expression, objective.
easy=[
('Soma das vendas',[12,8,15],'let resultado = 0;','resultado += {{x}};','resultado','somar todos os valores'),
('Produto acumulado',[2,3,4],'let resultado = 1;','resultado *= {{x}};','resultado','multiplicar todos os valores'),
('Contagem de pares',[2,5,8,9],'let resultado = 0;','if ({{x}} % 2 === 0) resultado++;','resultado','contar os números pares'),
('Valores positivos',[-2,4,0,9],'let resultado = [];','if ({{x}} > 0) resultado.push({{x}});','resultado','coletar os números positivos'),
('Dobro de cada item',[3,6,9],'let resultado = [];','resultado.push({{x}} * 2);','resultado','produzir os dobros'),
('Soma dos quadrados',[1,2,3],'let resultado = 0;','resultado += {{x}} ** 2;','resultado','somar os quadrados'),
('Maior temperatura',[18,25,21],'let resultado = -Infinity;','if ({{x}} > resultado) resultado = {{x}};','resultado','encontrar o maior valor'),
('Menor custo',[40,25,60],'let resultado = Infinity;','if ({{x}} < resultado) resultado = {{x}};','resultado','encontrar o menor valor'),
('Palavras em maiúsculas',['node','web','js'],'let resultado = [];','resultado.push({{x}}.toUpperCase());','resultado','converter todas as palavras para maiúsculas'),
('Tamanho das palavras',['sol','lua','planeta'],'let resultado = [];','resultado.push({{x}}.length);','resultado','coletar os comprimentos das palavras'),
('Total de caracteres',['ola','mundo'],'let resultado = 0;','resultado += {{x}}.length;','resultado','somar a quantidade de caracteres'),
('Palavras longas',['a','casa','computador'],'let resultado = [];','if ({{x}}.length > 4) resultado.push({{x}});','resultado','coletar palavras com mais de quatro letras'),
('Contar zeros',[0,2,0,3,0],'let resultado = 0;','if ({{x}} === 0) resultado++;','resultado','contar os zeros'),
('Subtrair despesas',[10,20,15],'let resultado = 100;','resultado -= {{x}};','resultado','descontar todas as despesas do saldo inicial de 100'),
('Inverter ordem',[1,2,3],'let resultado = [];','resultado.unshift({{x}});','resultado','construir a sequência na ordem inversa'),
('Montar uma frase',['Eu','estudo','Node'],'let resultado = "";','resultado += {{x}} + " ";','resultado.trim()','unir palavras com um espaço, sem espaço final'),
('Valores absolutos',[-3,0,7],'let resultado = [];','resultado.push(Math.abs({{x}}));','resultado','obter os valores absolutos'),
('Arredondar preços',[2.4,8.7,9.1],'let resultado = [];','resultado.push(Math.round({{x}}));','resultado','arredondar ao inteiro mais próximo'),
('Preços com imposto',[10,20,30],'let resultado = [];','resultado.push({{x}} * 1.1);','resultado','aplicar 10% de imposto'),
('Primeiras letras',['Ana','Bia','Caio'],'let resultado = "";','resultado += {{x}}[0];','resultado','juntar a primeira letra de cada nome'),
('Contar aprovados',[4,7,9,6],'let resultado = 0;','if ({{x}} >= 6) resultado++;','resultado','contar notas maiores ou iguais a seis'),
('Remover espaços',[' a ',' b','c '],'let resultado = [];','resultado.push({{x}}.trim());','resultado','retirar espaços externos de cada texto'),
('Detectar múltiplos de três',[2,3,6,7],'let resultado = [];','if ({{x}} % 3 === 0) resultado.push({{x}});','resultado','coletar múltiplos de três'),
('Verificar presença',[1,7,4],'let resultado = false;','if ({{x}} === 7) resultado = true;','resultado','informar se existe o número sete'),
('Contar ausências',[True,False,False,True],'let resultado = 0;','if (!{{x}}) resultado++;','resultado','contar os valores falsos'),
('Construir etiquetas',[1,2,3],'let resultado = [];','resultado.push("item-" + {{x}});','resultado','prefixar cada número com item-'),
('Converter para número',['12','8','3'],'let resultado = [];','resultado.push(Number({{x}}));','resultado','converter strings numéricas para números'),
('Acumular letras a',['ana','bia','casa'],'let resultado = 0;','resultado += {{x}}.split("a").length - 1;','resultado','contar ocorrências da letra a'),
('Separar negativos',[-8,3,-2,0],'let resultado = [];','if ({{x}} < 0) resultado.push({{x}});','resultado','coletar números negativos'),
('Total de itens',[2,4,6,8],'let resultado = 0;','resultado++;','resultado','contar itens sem consultar length no resultado'),
]
mediumloops=[
('Média das avaliações',[3,7,8,6],'let soma = 0, quantidade = 0;','soma += {{x}}; quantidade++;','quantidade ? soma / quantidade : 0','calcular a média, retornando zero se vazio'),
('Remover duplicados',[2,2,3,1,3],'let resultado = [];','if (!resultado.includes({{x}})) resultado.push({{x}});','resultado','remover duplicados preservando a primeira ocorrência'),
('Frequência de palavras',['azul','verde','azul'],'let resultado = Object.create(null);','resultado[{{x}}] = (resultado[{{x}}] || 0) + 1;','resultado','contar a frequência de cada palavra'),
('Somas prefixadas',[2,4,1,3],'let soma = 0, resultado = [];','soma += {{x}}; resultado.push(soma);','resultado','produzir a soma acumulada em cada posição'),
('Alternância de sinais',[1,2,3,4],'let resultado = 0, sinal = 1;','resultado += {{x}} * sinal; sinal *= -1;','resultado','somar alternando sinais, começando pelo positivo'),
('Separar por paridade',[1,2,3,4],'let resultado = { pares: [], impares: [] };','resultado[{{x}} % 2 === 0 ? "pares" : "impares"].push({{x}});','resultado','agrupar pares e ímpares'),
('Contagem acima da média',[2,4,6,8],'const media = dados.reduce((a,b) => a+b, 0) / dados.length; let resultado = 0;','if ({{x}} > media) resultado++;','resultado','contar os valores acima da média da entrada'),
('Maior palavra',['sol','universo','lua'],'let resultado = "";','if ({{x}}.length > resultado.length) resultado = {{x}};','resultado','encontrar a primeira palavra de maior comprimento'),
('Compactar consecutivos',[1,1,2,2,1],'let resultado = [];','if (!resultado.length || resultado[resultado.length - 1] !== {{x}}) resultado.push({{x}});','resultado','remover apenas duplicatas consecutivas'),
('Diferenças entre vizinhos',[3,8,6,10],'let anterior, resultado = [];','if (anterior !== undefined) resultado.push({{x}} - anterior); anterior = {{x}};','resultado','calcular diferenças entre itens consecutivos'),
('Maior sequência positiva',[1,2,-1,3,4,5],'let atual = 0, resultado = 0;','atual = {{x}} > 0 ? atual + 1 : 0; resultado = Math.max(resultado, atual);','resultado','medir a maior sequência consecutiva positiva'),
('Inventário por categoria',[{'tipo':'livro','qtd':2},{'tipo':'jogo','qtd':3},{'tipo':'livro','qtd':1}],'let resultado = Object.create(null);','resultado[{{x}}.tipo] = (resultado[{{x}}.tipo] || 0) + {{x}}.qtd;','resultado','somar quantidades por categoria'),
('Interseção sem repetição',[1,2,2,4],'const outros = [2,3,4]; let resultado = [];','if (outros.includes({{x}}) && !resultado.includes({{x}})) resultado.push({{x}});','resultado','encontrar a interseção com outros sem duplicatas'),
('Índice lógico de busca',['a','b','c'],'let pos = 0, resultado = -1;','if ({{x}} === "b" && resultado === -1) resultado = pos; pos++;','resultado','encontrar o índice da primeira letra b'),
('Agrupar por tamanho',['a','lua','sol','b'],'let resultado = Object.create(null);','(resultado[{{x}}.length] ??= []).push({{x}});','resultado','agrupar palavras pelo comprimento'),
('Somar matriz',[[1,2],[3,4]],'let resultado = 0;','for (const valor of {{x}}) resultado += valor;','resultado','somar todos os elementos da matriz'),
('Achatar um nível',[[1,2],[3],[4,5]],'let resultado = [];','resultado.push(...{{x}});','resultado','achatar um nível de arrays'),
('Encontrar segundo maior',[8,3,12,12,6],'let maior = -Infinity, segundo = -Infinity;','if ({{x}} > maior) { segundo = maior; maior = {{x}}; } else if ({{x}} < maior && {{x}} > segundo) segundo = {{x}};','segundo','encontrar o segundo maior valor distinto'),
('Validar ordem',[1,3,2,5],'let anterior = -Infinity, resultado = true;','if ({{x}} < anterior) resultado = false; anterior = {{x}};','resultado','testar ordem não decrescente'),
('Produto sem zeros',[2,0,3,0,4],'let resultado = 1;','if ({{x}} !== 0) resultado *= {{x}};','resultado','multiplicar os valores não nulos'),
('Contar mudanças de sinal',[-2,3,4,-1,5],'let anterior = 0, resultado = 0;','if ({{x}} !== 0) { if (anterior !== 0 && Math.sign(anterior) !== Math.sign({{x}})) resultado++; anterior = {{x}}; }','resultado','contar mudanças de sinal ignorando zeros'),
('Saldo com limite',[20,-50,10,-90],'let resultado = 100;','resultado = Math.max(0, resultado + {{x}});','resultado','aplicar movimentos mantendo saldo mínimo zero'),
('Média ponderada',[{'nota':7,'peso':2},{'nota':9,'peso':3}],'let soma = 0, pesos = 0;','soma += {{x}}.nota * {{x}}.peso; pesos += {{x}}.peso;','soma / pesos','calcular a média ponderada'),
('Normalizar identificadores',[' Ana ','BIA',' caio'],'let resultado = [];','resultado.push({{x}}.trim().toLowerCase().replaceAll(" ", "-"));','resultado','retirar espaços externos, usar minúsculas e trocar espaços internos por hífens'),
('Primeiro não repetido',['a','b','a','c'],'const freq = Object.create(null); let ordem = [];','freq[{{x}}] = (freq[{{x}}] || 0) + 1; ordem.push({{x}});','ordem.find(v => freq[v] === 1) ?? null','encontrar o primeiro elemento com frequência um'),
('Custos por desconto',[120,40,200],'let resultado = 0;','resultado += {{x}} >= 100 ? {{x}} * 0.9 : {{x}};','resultado','somar preços com desconto de 10% nos valores de pelo menos 100'),
('Lotes de três',[1,2,3,4,5],'let resultado = [], lote = [];','lote.push({{x}}); if (lote.length === 3) { resultado.push(lote); lote = []; }','lote.length ? [...resultado, lote] : resultado','dividir em lotes de três, incluindo sobra'),
('Pontuação de torneio',['V','E','D','V'],'let resultado = 0;','resultado += {{x}} === "V" ? 3 : {{x}} === "E" ? 1 : 0;','resultado','atribuir três pontos à vitória, um ao empate e zero à derrota'),
('Histograma por faixa',[12,25,8,32,19],'let resultado = Object.create(null);','const faixa = Math.floor({{x}} / 10) * 10; resultado[faixa] = (resultado[faixa] || 0) + 1;','resultado','contar números por dezenas: 0–9, 10–19 etc.'),
('Juros compostos variáveis',[0.01,0.02,0.015],'let resultado = 1000;','resultado *= 1 + {{x}};','Number(resultado.toFixed(2))','aplicar as taxas sucessivas e arredondar só ao final'),
]
hardloops=[
('Subarray máximo',[-2,1,-3,4,-1,2,1,-5,4],'let atual = 0, resultado = -Infinity;','atual = Math.max({{x}}, atual + {{x}}); resultado = Math.max(resultado, atual);','resultado','aplicar Kadane e encontrar a maior soma de subarray não vazio'),
('Lucro de uma negociação',[7,1,5,3,6,4],'let menor = Infinity, resultado = 0;','menor = Math.min(menor, {{x}}); resultado = Math.max(resultado, {{x}} - menor);','resultado','maximizar o lucro de uma compra seguida de uma venda'),
('Equilíbrio de parênteses',list('(()())'),'let saldo = 0, valido = true;','saldo += {{x}} === "(" ? 1 : -1; if (saldo < 0) valido = false;','valido && saldo === 0','validar o balanceamento dos parênteses'),
('Pilha de delimitadores',list('{[()]}'),'const pares = { ")": "(", "]": "[", "}": "{" }; let pilha = [], valido = true;','if ("([{ ".trim().includes({{x}})) pilha.push({{x}}); else if (pilha.pop() !== pares[{{x}}]) valido = false;','valido && pilha.length === 0','validar delimitadores aninhados de três tipos'),
('Codificação de sequências',list('aaabbc'),'let resultado = [], anterior, qtd = 0;','if ({{x}} === anterior) qtd++; else { if (qtd) resultado.push([anterior, qtd]); anterior = {{x}}; qtd = 1; }','qtd ? [...resultado, [anterior, qtd]] : resultado','codificar sequências como pares de caractere e frequência'),
('Janela móvel de três',[2,1,5,1,3,2],'let fila = [], soma = 0, resultado = -Infinity;','fila.push({{x}}); soma += {{x}}; if (fila.length > 3) soma -= fila.shift(); if (fila.length === 3) resultado = Math.max(resultado, soma);','resultado','encontrar a maior soma de três elementos consecutivos'),
('Dois números com soma alvo',[2,7,11,15],'const alvo = 9; let vistos = new Set(), resultado = false;','if (vistos.has(alvo - {{x}})) resultado = true; vistos.add({{x}});','resultado','detectar dois itens distintos que somam nove'),
('Subsequência crescente',[10,9,2,5,3,7,101,18],'let caudas = [];','let l = 0, r = caudas.length; while (l < r) { const m = (l + r) >> 1; if (caudas[m] < {{x}}) l = m + 1; else r = m; } caudas[l] = {{x}};','caudas.length','obter o comprimento da maior subsequência estritamente crescente em O(n log n)'),
('Fusão de intervalos',[[1,3],[2,6],[8,10],[9,12]],'let resultado = [];','const ultimo = resultado[resultado.length - 1]; if (ultimo && {{x}}[0] <= ultimo[1]) ultimo[1] = Math.max(ultimo[1], {{x}}[1]); else resultado.push([...{{x}}]);','resultado','fundir intervalos previamente ordenados por início'),
('Produto máximo de subarray',[2,3,-2,4],'let maximo = 1, minimo = 1, resultado = -Infinity;','const a = maximo * {{x}}, b = minimo * {{x}}; maximo = Math.max({{x}}, a, b); minimo = Math.min({{x}}, a, b); resultado = Math.max(resultado, maximo);','resultado','encontrar o maior produto de um subarray não vazio'),
('Variância incremental',[2,4,4,4,5,5,7,9],'let n = 0, media = 0, m2 = 0;','n++; const delta = {{x}} - media; media += delta / n; m2 += delta * ({{x}} - media);','m2 / n','calcular variância populacional pelo método de Welford'),
('Votação de maioria',[2,2,1,2,3,2,2],'let candidato, votos = 0;','if (votos === 0) candidato = {{x}}; votos += {{x}} === candidato ? 1 : -1;','candidato','encontrar a maioria com Boyer–Moore; a entrada garante maioria absoluta'),
('Avaliar notação pós-fixa',['2','3','+','4','*'],'let pilha = [];','if (["+", "*"].includes({{x}})) { const b = pilha.pop(), a = pilha.pop(); pilha.push({{x}} === "+" ? a + b : a * b); } else pilha.push(Number({{x}}));','pilha[0]','avaliar uma expressão pós-fixa válida com + e *'),
('Contar subarrays com soma zero',[1,-1,2,-2,3],'let soma = 0, freq = new Map([[0,1]]), resultado = 0;','soma += {{x}}; resultado += freq.get(soma) || 0; freq.set(soma, (freq.get(soma) || 0) + 1);','resultado','contar subarrays de soma zero com frequências de prefixos'),
('Próximo maior elemento',[2,1,3,4],'let pilha = [], resultado = [], pos = 0;','while (pilha.length && pilha[pilha.length - 1].valor < {{x}}) resultado[pilha.pop().pos] = {{x}}; pilha.push({ valor: {{x}}, pos }); resultado[pos++] = -1;','resultado','usar pilha monotônica para obter o próximo maior à direita; -1 se ausente'),
('Reservatório determinístico',[8,3,5,2,9],'let resultado = [], pos = 0;','pos++; if (resultado.length < 3) resultado.push({{x}}); else { const j = (pos * 7) % pos; if (j < 3) resultado[j] = {{x}}; }','resultado','simular reservatório de tamanho três com índice determinístico j = (pos * 7) % pos; não é amostragem aleatória'),
('Programação de tarefas',[{'prazo':2,'duracao':1},{'prazo':4,'duracao':2},{'prazo':5,'duracao':3}],'let tempo = 0, resultado = [];','if (tempo + {{x}}.duracao <= {{x}}.prazo) { tempo += {{x}}.duracao; resultado.push({{x}}.prazo); }','resultado','aceitar na ordem apenas tarefas que ainda cabem em seus prazos'),
('Distintos por janela',[1,2,1,3,4],'let fila = [], freq = new Map(), resultado = [];','fila.push({{x}}); freq.set({{x}}, (freq.get({{x}}) || 0) + 1); if (fila.length > 3) { const saiu = fila.shift(); freq.set(saiu, freq.get(saiu) - 1); if (!freq.get(saiu)) freq.delete(saiu); } if (fila.length === 3) resultado.push(freq.size);','resultado','contar elementos distintos em cada janela de tamanho três'),
('Decodificar comprimentos',[['a',3],['b',2],['c',1]],'let resultado = "";','resultado += {{x}}[0].repeat({{x}}[1]);','resultado','decodificar os pares caractere–quantidade'),
('Intercalar contagens',[{'a':2,'b':1},{'a':1,'b':3}],'let resultado = [];','let a = {{x}}.a, b = {{x}}.b; while (a > 0 || b > 0) { if (a-- > 0) resultado.push("A"); if (b-- > 0) resultado.push("B"); }','resultado.join("")','para cada par, alternar A e B até consumir ambas as contagens'),
('MDC acumulado',[48,18,30],'let resultado = 0;','let a = resultado, b = {{x}}; while (b) { [a, b] = [b, a % b]; } resultado = a;','resultado','calcular o máximo divisor comum de todos os números'),
('MMC acumulado',[4,6,10],'let resultado = 1;','let a = resultado, b = {{x}}; while (b) [a, b] = [b, a % b]; resultado = resultado / a * {{x}};','resultado','calcular o mínimo múltiplo comum dos inteiros positivos'),
('Conversão de base',[1,0,1,1],'let resultado = 0;','resultado = resultado * 2 + {{x}};','resultado','interpretar a sequência de bits como inteiro binário'),
('Hash polinomial',list('node'),'let resultado = 0;','resultado = (resultado * 31 + {{x}}.charCodeAt(0)) % 1000000007;','resultado','calcular hash polinomial com base 31 e módulo 1000000007'),
('União de conjuntos',[[1,2],[2,3],[3,4]],'let resultado = new Set();','for (const valor of {{x}}) resultado.add(valor);','[...resultado]','unir todos os conjuntos preservando ordem de primeira aparição'),
('Matriz transposta',[[1,2,3],[4,5,6]],'let resultado = [], linha = 0;','for (let coluna = 0; coluna < {{x}}.length; coluna++) { (resultado[coluna] ??= [])[linha] = {{x}}[coluna]; } linha++;','resultado','transpor uma matriz retangular'),
('Diagonais da matriz',[[1,2,3],[4,5,6],[7,8,9]],'let principal = 0, secundaria = 0, linha = 0;','principal += {{x}}[linha]; secundaria += {{x}}[dados.length - 1 - linha]; linha++;','[principal, secundaria]','somar as diagonais principal e secundária separadamente'),
('Agrupar anagramas',['amor','roma','casa','saca','lua'],'let grupos = new Map();','const chave = {{x}}.split("").sort().join(""); if (!grupos.has(chave)) grupos.set(chave, []); grupos.get(chave).push({{x}});','[...grupos.values()]','agrupar palavras que são anagramas'),
('Distância de percurso',[[0,0],[3,4],[6,4]],'let anterior, resultado = 0;','if (anterior) resultado += Math.hypot({{x}}[0] - anterior[0], {{x}}[1] - anterior[1]); anterior = {{x}};','resultado','somar a distância euclidiana entre pontos consecutivos'),
('Substring sem repetição',list('abcabcbb'),'let janela = [], resultado = 0;','while (janela.includes({{x}})) janela.shift(); janela.push({{x}}); resultado = Math.max(resultado, janela.length);','resultado','encontrar o comprimento da maior substring sem caracteres repetidos'),
]
levels=['easy','medium','hard']; topics=['if','if-else','else-if','switch','ternary','for','while','do-while','for-of','for-in']; result=[]
def blank(code,answer,n=0):
    assert answer in code,(code,answer)
    return code.replace(answer,'___'+str(n)+'___',1)
for li, recipes in enumerate([decisions,medium,hard]):
 for topic in topics[:5]:
  for i,rec in enumerate(recipes):
   title,var,value,condition,rule=rec[:5]
   prefix=f'const {var} = {json.dumps(value,ensure_ascii=False)};\n'
   if topic=='if':
    code=prefix+'let resultado = "não atende";\nif (___0___) {\n  resultado = "atende";\n}\nconsole.log(resultado);'; answer=condition; goal=f'Faça a condição ser verdadeira quando {rule}.'
   elif topic=='if-else':
    code=prefix+'let resultado;\nif (___0___) {\n  resultado = "aceito";\n} else {\n  resultado = "recusado";\n}\nconsole.log(resultado);';answer=condition;goal=f'Decida entre aceito e recusado: aceite quando {rule}.'
   elif topic=='else-if':
    code=prefix+f'const regra = ({condition});\nconst revisao = {str(i%2==0).lower()};\nlet resultado;\nif (regra && !revisao) {{\n  resultado = "automático";\n}} else if (___0___) {{\n  resultado = "revisar";\n}} else {{\n  resultado = "recusado";\n}}\nconsole.log(resultado);';answer='regra && revisao';goal=f'A regra principal verifica se {rule}. Classifique como revisar quando a regra for válida e a revisão estiver ativa; caso contrário, recuse.'
   elif topic=='switch':
    code=prefix+f'const regra = ({condition});\nconst revisao = {str(i%2==0).lower()};\nconst estado = regra ? (revisao ? "pendente" : "liberado") : "negado";\nlet resultado;\nswitch (estado) {{\n  case "liberado":\n    resultado = 200;\n    ___0___;\n  case "pendente":\n    resultado = 202;\n    break;\n  ___1___:\n    resultado = 403;\n}}\nconsole.log(resultado);';answer=['break','default'];goal=f'O estado vem da regra: {rule}. Evite que o caso liberado continue executando outros casos e cubra estados não reconhecidos.'
   else:
    code=prefix+'const resultado = (___0___) ? "sim" : "não";\nconsole.log(resultado);';answer=condition;goal=f'Use uma expressão condicional para responder sim quando {rule}.'
   answers=answer if isinstance(answer,list) else [answer]
   result.append(dict(id=f'{topic}-{levels[li]}-{i+1:02}',topic=topic,level=levels[li],number=i+1,title=title,description=goal,code=code,answers=[[a] for a in answers],hint=('O switch precisa de break para encerrar um caso e default para o caso padrão.' if topic=='switch' else 'Use regra && revisao para combinar as duas condições.' if topic=='else-if' else f'Observe a regra com atenção: {rule}. Use {rec[5] if len(rec)>5 else "operadores lógicos e comparações"}.'),explanation=f'A condição usada nesta solução é {condition}. '+('O encadeamento distingue aprovação direta, revisão e recusa.' if topic=='else-if' else 'Cada ramo produz uma saída diferente conforme a regra.')))
for li,recipes in enumerate([easy,mediumloops,hardloops]):
 for topic in topics[5:]:
  for i,(title,data,init,body,out,goal) in enumerate(recipes):
   prefix=f'const dados = {json.dumps(data,ensure_ascii=False)};\n{init}\n'
   # A blank always belongs to traversal; more challenging levels also complete
   # the algorithm body, rather than only changing traversal punctuation.
   if topic=='for':
    loop='for (let i = 0; ___0___; i++) {\n  const item = dados[i];\n  BODY\n}';answer='i < dados.length'
   elif topic=='while':
    loop='let i = 0;\nwhile (___0___) {\n  const item = dados[i];\n  BODY\n  i++;\n}';answer='i < dados.length'
   elif topic=='do-while':
    loop='let i = 0;\nif (dados.length > 0) {\n  do {\n    const item = dados[i];\n    BODY\n    i++;\n  } while (___0___);\n}';answer='i < dados.length'
   elif topic=='for-of':
    loop='for (const item ___0___ dados) {\n  BODY\n}';answer='of'
   else:
    prefix=f'const dados = {json.dumps(data,ensure_ascii=False)};\nconst registro = Object.fromEntries(dados.map((v, i) => ["item" + i, v]));\n{init}\n'
    loop='for (const campo ___0___ registro) {\n  if (!Object.hasOwn(registro, campo)) continue;\n  const item = registro[campo];\n  BODY\n}';answer='in'
   resolved=body.replace('{{x}}','item')
   # Easy exercises complete one data expression; medium/hard complete the full
   # algorithm statement alongside traversal to practice reasoning explicitly.
   if li==0:
    if 'item' in resolved:
     authored=resolved.replace('item','___1___',1);second='item'
    else: authored='___1___;';second='resultado++'
   else: authored='___1___';second=resolved
   code=prefix+loop.replace('BODY',authored)+'\nconsole.log(JSON.stringify('+out+'));'
   result.append(dict(id=f'{topic}-{levels[li]}-{i+1:02}',topic=topic,level=levels[li],number=i+1,title=title,description=f'Use {topic.replace("-","…")} para {goal}. Preserve a ordem da entrada. '+('Complete a condição de parada e a lógica dentro do laço.' if topic in ['for','while','do-while'] else 'Complete o operador de iteração e a lógica dentro do laço.'),code=code,answers=[[answer],[second]],hint=f'{"O índice deve permanecer menor que dados.length." if topic in ["for","while","do-while"] else "for…of percorre valores; for…in percorre chaves."} Dentro do laço, item representa o valor atual. '+f'Objetivo: {goal}.',explanation=f'A lógica do passo é: {resolved} O acumulador guarda informação entre as iterações.'))
# Vary the decision operation itself, retaining the subject as an explicit review trail.
for e in result:
 if e['topic']=='else-if':
  condition=e['code'].split('const regra = (',1)[1].split(');\nconst revisao',1)[0]
  prefix=e['code'].split('const regra = (',1)[0]
  review=str(e['number']%2==1).lower()
  e['code']=prefix+f'const revisao = {review};\nlet resultado;\nif (!({condition})) {{\n  resultado = "recusado";\n}} else if (___0___) {{\n  resultado = "revisar";\n}} else {{\n  resultado = "automático";\n}}\nconsole.log(resultado);'
  e['answers']=[[f'({condition}) && revisao',f'revisao && ({condition})','revisao']]
  e['hint']='O primeiro ramo já rejeita entradas inválidas. No segundo, verifique se revisao está ativa; você também pode repetir a regra com &&.'
  e['title']='Triagem: '+e['title']
 elif e['topic']=='switch':
  condition=e['code'].split('const regra = (',1)[1].split(');\nconst revisao',1)[0]
  prefix=e['code'].split('const regra = (',1)[0]
  e['code']=prefix+'let resultado;\nswitch (true) {\n  case (___0___):\n    resultado = 200;\n    ___1___;\n  default:\n    resultado = 403;\n}\nconsole.log(resultado);'
  e['answers']=[[condition],['break']]
  e['description']='Use switch (true) para retornar 200 quando a regra é satisfeita, ou 403 caso contrário. Regra: '+e['explanation'].split('A condição usada nesta solução é ',1)[1].split('. Cada ramo')[0]+'. Complete a condição e encerre o caso sem cair no padrão.'
  e['hint']='Em switch (true), o case deve ser uma expressão booleana. break impede continuar até default.'
  e['title']='Roteamento: '+e['title']
 elif e['topic']=='if-else':
  condition=e['answers'][0][0]
  e['answers']=[[f'!({condition})']]
  e['code']=e['code'].replace('resultado = "aceito"','resultado = "recusado"',1)
  at=e['code'].index('} else {')
  e['code']=e['code'][:at]+e['code'][at:].replace('resultado = "recusado"','resultado = "aceito"',1)
  e['description']+=' Complete a condição de RECUSA no primeiro ramo: negue a regra de aceitação com !.'
  e['hint']='Agrupe a regra inteira entre parênteses e use ! para negá-la. '+e['hint']
  e['title']='Recusa: '+e['title']
 elif e['topic']=='ternary':
  e['title']='Resposta direta: '+e['title']

assert len(result)==900
assert len({x['id'] for x in result})==900
Path('lib/exercises.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('900 exercícios gerados: 30 por estrutura e nível.')
