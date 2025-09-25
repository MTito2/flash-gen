# Flash-Gen – Criação Automática de Flashcards com IA  

Este projeto automatiza a criação de flashcards para o Anki usando inteligência artificial e imagens. Ele integra a API da OpenAI para gerar conteúdo dos flashcards, a API da Unsplash para obter imagens e os add-ons do Anki para automatizar a inclusão dos cards.  

## ✨ Motivação  
Comecei a estudar inglês recentemente e percebi que criar flashcards manualmente é um processo entediante e lento, o que pode atrapalhar a construção de um novo hábito. Após testar ferramentas prontas e encontrar custos altos ou limitações, encontrei a solução no Python.  

## 🛠️ Tecnologias Utilizadas  
- **API da OpenAI**: Criação de conteúdo para os flashcards.  
- **API da Unsplash**: Busca de imagens para ilustrar palavras e expressões.  
- **Add-ons do Anki**: Automação na adição e visualização dos flashcards.  

## 📚 Fluxo do Sistema  
1. O usuário fornece palavras ou expressões que deseja aprender.  
2. A IA gera tradução, exemplos, variações e notas sobre cada termo.  
3. Se a palavra for representável visualmente, é feita uma busca na Unsplash.  
4. As informações e a imagem são incluídas automaticamente no Anki.  

## 💡 Por que isso é incrível  
Esse projeto mostra como a programação pode resolver problemas do dia a dia que ferramentas prontas nem sempre conseguem. Além de resolver o problema, o desenvolvimento traz aprendizado valioso em Python, automação e integração de APIs.  

## 📝 Prompt Utilizado  

```text
Você receberá uma ou mais palavras ou expressões separadas por vírgulas.

Regras:
front: apenas a palavra ou expressão recebida. Aplique a formatação com a primeira letra em maiúsculo

back:  Aplique a formatação com a primeira letra em maiúsculo, todo o HTML deve estar em uma linha, com 3 exemplos de frases no formato “Inglês — Tradução em português”.

Tradução: Forneça a tradução da palavra ou expressão. (Colocando a primeira letra em maiúsculo)

Variações possíveis:
- Se for verbo: liste formas no presente, passado, futuro, além dos aspectos (simples, contínuo, perfeito e perfeito contínuo).
- Se for substantivo: liste singular, plural e posse.
- Se for adjetivo ou advérbio: liste grau positivo, comparativo e superlativo (quando aplicável).
- Se for pronome: liste as formas por caso (sujeito, objeto, possessivo).
- Se for determinante: liste singular, plural e formas possessivas (quando houver).
- Se não houver variação, não adicione nada.

Notas:  
- Dê um breve comentário sobre o uso da palavra ou expressão, como:  
  - contexto cultural (quando for relevante),  
  - registro (formal, informal, gíria),  
  - collocations comuns (palavras que normalmente aparecem juntas),  
  - expressões idiomáticas que envolvem essa palavra.  
- Se não houver nada de relevante, não adicione nada.

Use apenas tags <div>, <p>, <b>, <ul>, <li>.
possible_img: true para palavras concretas; false para expressões idiomáticas, verbos abstratos ou conceitos difíceis de ilustrar.

JSON final: string JSON válida, pronta para json.loads() no Python.
Campos do modelo Anki em português: use "Frente" e "Verso" para modelo "Básico".

Para cada termo, gere uma lista de dicionários Python no formato:
[
    {
        "front": "palavra_ou_expressão",
        "back": "<div><p><b>Tradução:</b> <b>palavra principal em negrito</b></p><p><b>Variações possíveis:</b> ...</p><p><b>Exemplos:</b><ul><li>Exemplo 1 — Tradução</li><li>Exemplo 2 — Tradução</li><li>Exemplo 3 — Tradução</li></ul></p><p><b>Notas:</b> ...</p></div>",
        "possible_img": true ou false
    }
]
