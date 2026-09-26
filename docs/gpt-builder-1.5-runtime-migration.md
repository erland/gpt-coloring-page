# GPT Byggaren 1.5.0 – migreringsplan

Projekt: **Målarbilds-generatorn**

## Utgångsläge

Projektet är ett fungerande legacy-GPT-projekt med:
- version **1.0.0**
- huvudinstruktion i `gpt-instructions.md`
- **3 Knowledge-filer**
- Custom GPT- och Chat ZIP-distribution
- Image generation som kritisk capability
- A4-layout, åldersanpassning och tydliga fallback-regler som kärnbeteende

## Preserve-first

Migreringen ska bevara:
- instruktionen byte-identiskt tills canonical-källan är etablerad,
- 3/3 Knowledge-filer,
- A4 portrait som standardformat,
- de två formatlägena (endast målarbild / referens + målarbild),
- åldersanpassad detaljnivå,
- reglerna för ren svartvit målarbild utan gråskala/skuggning,
- Image generation som kritisk capability,
- fallback-beteendet vid kända figurer/varumärken,
- version **1.0.0**,
- befintliga Chat- och Custom GPT-distributioner.

## Runtime-målbild

### Aktiva baseline-runtimes
1. ChatGPT Chat
2. ChatGPT Custom GPT

### Ska bedömas
- Claude Projects
- OpenCode
- OpenAI Plugin

Ytterligare runtimes får endast aktiveras om de kan uppfylla den kritiska bildgenereringscapabilityn utan att försvaga produktbeteendet.

## Steg

### 1. Baseline och canonical källa
Inför `gpt-project.yaml`, separat migrationsstatus och canonical `assistant/instructions.md` utan beteendeförändring.

### 2. Normalisera GPT Byggaren 1.5-kontrakten
Definiera capability-, artifact-, workspace/state- och tool-kontrakt och lägg maskinell validering.

### 3. Normalisera Chat och Custom GPT
Bygg båda från canonical projektdata och verifiera 3/3 Knowledge samt kritiska bildregler.

### 4. Bedöm Claude Projects och OpenCode
Gör explicit parity-bedömning. Aktivera endast om kritisk Image generation-parity är verklig.

### 5. Bedöm OpenAI Plugin
Bedöm skills-first-parity för bildflöde och ev. state/artefakter.

### 6. Generalisera build, parity, CI och release
Inför deklarativ runtime-registry och låt aktivt distributionsset härledas därifrån.

### 7. Slutlig readiness och dokumentationssynk
Synka README, lägg final hygiene och explicit 7/7-migrationsgate.

## Klart-kriterium

Migreringen är klar när:
- canonical beteende är bevarat,
- 3/3 Knowledge är bevarade,
- Chat och Custom GPT verifieras från samma canonical källa,
- övriga runtimes har explicit compatibilitybeslut,
- build/CI/release inte har dolda hårdkodade runtime-antaganden,
- VERSION fortfarande är **1.0.0**,
- slutlig CI är grön.
