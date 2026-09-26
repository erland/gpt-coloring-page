# OpenAI Plugin – compatibility assessment

Projekt: **Målarbilds-generatorn**  
GPT Byggaren: **1.5.0**

## Slutsats

OpenAI Plugin bedöms som **reduced**, **advisory-only** och lämnas **inte aktiv**.

Projektets kärna är att faktiskt skapa utskrivbara målarbilder med Image generation. Pluginens skills/reference-material kan bära instruktion, Knowledge, åldersregler, layoutregler och fallbacklogik, men full runtime-parity kan inte garanteras för den faktiska bildartefakten utan motsvarande bildverktyg.

## Parity-bedömning

| Område | Bedömning |
|---|---|
| Behavior | reduced |
| Capability | reduced |
| Artifact | reduced |
| Workspace/state | equivalent |
| Tool | reduced |

### Behavior

Instruktionerna kan representeras som skills, men kärnbeteendet är inte enbart rådgivning. Slutresultatet ska vara en faktiskt genererad A4-målarbild.

### Capability

Kritisk capability:
- `image_generation`

Utan garanterad tillgång till motsvarande bildgenerering är pluginen inte equivalent.

### Artifact

Markdown, Knowledge och prompt-/layoutregler kan representeras. Den obligatoriska användarartefakten — en faktiskt genererad utskrivbar bild — kan däremot inte behandlas som guaranteed equivalent.

### Workspace/state

State-kraven är enkla: aktuell motivbeskrivning, ålder/svårighetsnivå och valt layoutläge. Dessa kan representeras utan större problem.

### Tool

Plugin v1 får inte:
- påstå att en bild har skapats när ingen Image generation körts,
- ersätta bildgenerering med en textprompt och kalla det färdig leverans,
- försvaga reglerna för A4 portrait, max 25 % referensbild, svartvit coloring-del eller åldersanpassning.

## Aktiveringsbeslut

- status: `assessed_not_active`
- compatibility: `reduced`
- advisory_only: `true`
- blocker: `critical_image_generation_not_guaranteed`

Ingen Plugin-distribution byggs eller publiceras i denna migrering.

## Framtida omprövning

Plugin kan omprövas när runtime kan uppfylla samma canonical kontrakt för:
1. faktisk Image generation,
2. A4 portrait-layout,
3. svartvit målarbild utan gråskala/skuggning,
4. referensläge med max 25 % sidhuvud,
5. åldersanpassning,
6. samma fallback-beteende.

Ingen canonical produktregel ändras av denna bedömning.
