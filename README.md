# Logic Lab

Laboratório pessoal em português com 1.350 exercícios de lacunas: 30 por nível (fácil, médio e difícil) em 15 assuntos: if, if/else, else if, switch, ternário, for, while, do/while, for/of, for/in, return, try/catch, async/await, arrays e objetos.


Ordem sugerida de estudo: if → if/else → else if → switch → ternário → return → arrays → objetos → for → while → do/while → for/of → for/in → try/catch → async/await. A navegação e os gráficos seguem a mesma ordem; cada assunto mantém os três níveis. Os fundamentos de coleções aparecem antes dos laços especializados, e o retorno de funções antes dos callbacks.

## Usar

Preencha as lacunas e clique em Verificar resposta. Cada envio completo registra um acerto ou erro no banco SQLite/D1. Tentar novamente inicia outra tentativa; repetir requisições com o mesmo identificador não duplica registros. Ver gabarito é modo estudo e não registra acerto. Copiar código inclui as respostas atuais; Baixar .js salva um arquivo para executar com Node.js no VS Code.

A aba Aprendizado distingue exercícios únicos concluídos, tentativas e revisões. Datas usam America/Sao_Paulo. A proficiência combina cobertura, dificuldade e taxa de acerto, com fórmula explicada na interface. O site é pessoal e sua publicação permanece privada; o banco contém um único histórico do proprietário. Não ampliar para múltiplos usuários sem adicionar segregação por identidade.

## Correção e conteúdo

A correção compara tokens com gabaritos, aceitando espaços e aspas simples/duplas. Não executa código enviado ao servidor e não reconhece automaticamente todas as expressões semanticamente equivalentes. Há 90 regras de decisão e 90 algoritmos de repetição, revisitados nas diferentes estruturas para permitir comparação; os 30 desafios dentro de cada combinação de estrutura e nível têm objetivos distintos.

Os 270 exercícios de return, try/catch e async/await têm títulos e programas distintos, com 30 de cada dificuldade por assunto. Operações externas assíncronas são simuladas, sem rede ou credenciais. Seus oráculos são valores declarados separadamente dos gabaritos no arquivo autoral.

Os 180 exercícios de arrays e objetos ficam em `lib/collections-exercises.json`, gerados por `scripts/collections-topics.mjs`. São 30 por dificuldade em cada assunto, com títulos, programas e objetivos próprios. Seus resultados esperados também são declarados independentemente dos gabaritos.

## Executar localmente

Requer Node.js 22.13 ou posterior.

```sh
npm ci
npm run build
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_living_mister_sinister.sql
npm run dev -- --host 127.0.0.1 --port 5173
```

Aplique a migração apenas uma vez por banco local. Dados locais ficam em `.wrangler/state`; dados publicados usam D1 separado. O catálogo original está em `lib/exercises.json` e as novas categorias em `lib/additional-exercises.json`, com autoria em `scripts/new-topics.mjs`, e os contadores são derivados da tabela `attempts`.

## Validar catálogo

```sh
node scripts/new-topics.mjs
node scripts/collections-topics.mjs
node scripts/validate-exercises.mjs
npx tsc --noEmit
```

O validador é somente leitura: confere 1.350 exercícios e 45 grupos de 30, IDs, lacunas e unicidade dos novos títulos/códigos; executa gabaritos e alternativas com limite de tempo, aguarda Promises e compara as saídas aos oráculos. Também verifica rejeição de lacunas incorretas ou ausentes. Os 900 antigos passam por regressão contra as saídas preexistentes; isso não equivale a uma nova auditoria pedagógica completa. O teste nunca recalcula o esperado a partir da solução. O gerador legado Python não deve ser executado sobre o catálogo publicado sem uma revisão das saídas e IDs.

WebMCP: `open_exercise` permite abrir um exercício sem submeter respostas; só é registrado em navegadores com suporte.
