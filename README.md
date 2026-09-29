# Logic Lab

Laboratório pessoal em português com 900 exercícios de lacunas: 30 por nível (fácil, médio e difícil) em 10 estruturas: if, if/else, else if, switch, ternário, for, while, do/while, for/of e for/in.

## Usar

Preencha as lacunas e clique em Verificar resposta. Cada envio completo registra um acerto ou erro no banco SQLite/D1. Tentar novamente inicia outra tentativa; repetir requisições com o mesmo identificador não duplica registros. Ver gabarito é modo estudo e não registra acerto. Copiar código inclui as respostas atuais; Baixar .js salva um arquivo para executar com Node.js no VS Code.

A aba Aprendizado distingue exercícios únicos concluídos, tentativas e revisões. Datas usam America/Sao_Paulo. A proficiência combina cobertura, dificuldade e taxa de acerto, com fórmula explicada na interface. O site é pessoal e sua publicação permanece privada; o banco contém um único histórico do proprietário. Não ampliar para múltiplos usuários sem adicionar segregação por identidade.

## Correção e conteúdo

A correção compara tokens com gabaritos, aceitando espaços e aspas simples/duplas. Não executa código enviado ao servidor e não reconhece automaticamente todas as expressões semanticamente equivalentes. Há 90 regras de decisão e 90 algoritmos de repetição, revisitados nas diferentes estruturas para permitir comparação; os 30 desafios dentro de cada combinação de estrutura e nível têm objetivos distintos.

## Executar localmente

Requer Node.js 22.13 ou posterior.

```sh
npm ci
npm run build
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_living_mister_sinister.sql
npm run dev -- --host 127.0.0.1 --port 5173
```

Aplique a migração apenas uma vez por banco local. Dados locais ficam em `.wrangler/state`; dados publicados usam D1 separado. O catálogo está em `lib/exercises.json`, o gerador em `scripts/generate-exercises.py`, e os contadores são derivados da tabela `attempts`.

## Validar catálogo

```sh
python3 scripts/generate-exercises.py
node scripts/validate-exercises.mjs
npx tsc --noEmit
```

O validador confere quantidade, grupos, IDs e lacunas e executa os 900 gabaritos com limite de tempo. Ele também atualiza a saída esperada de cada exercício. Sempre rode-o depois do gerador.

WebMCP: `open_exercise` permite abrir um exercício sem submeter respostas; só é registrado em navegadores com suporte.
