# Claude Projects och OpenCode – runtime compatibility

Projekt: **Målarbilds-generatorn**  
GPT Byggaren: **1.5.0**

## Slutsats

Både Claude Projects och OpenCode bedöms som **reduced** och lämnas **inte aktiva** i denna migrering.

Projektets kärna är faktisk bildgenerering av utskrivbara A4-målarbilder. Textinstruktioner, Knowledge och layoutregler kan representeras i båda kandidaterna, men full parity kräver att runtime faktiskt kan skapa motsvarande bildartefakt och följa samma regler för A4-layout, åldersanpassning, svartvit målarbild och referensläge.

## Parity-bedömning

| Område | Claude Projects | OpenCode |
|---|---|---|
| Behavior | reduced | reduced |
| Capability | reduced | reduced |
| Artifact | reduced | reduced |
| Workspace/state | equivalent | equivalent |
| Tool | reduced | reduced |

### Claude Projects

Instruktion, Knowledge och dialogflöde kan representeras. Den kritiska Image generation-capabilityn kan däremot inte behandlas som garanterat equivalent för detta projekts faktiska bildleverans.

Beslut:
- compatibility: `reduced`
- activation: `not_active`
- blocker: `critical_image_generation_not_guaranteed`

### OpenCode

OpenCode kan bära instruktioner, filer och projektstruktur, men är inte en fullvärdig bildgenereringsruntime för detta användningsfall. Kodgenererad SVG/HTML eller andra programmatisk ersättningar skulle dessutom ändra produktens kärnbeteende.

Beslut:
- compatibility: `reduced`
- activation: `not_active`
- blocker: `critical_image_generation_not_guaranteed`

## Artifact-parity

Text, Markdown och Knowledge kan representeras. Den obligatoriska slutartefakten är däremot en faktiskt genererad utskrivbar bild, och den delen är reducerad utan säker Image generation-parity.

## Workspace/state

Projektet har relativt enkelt state och båda kandidaterna kan bära nuvarande krav, men detta räcker inte för aktivering när den kritiska bildcapabilityn saknas.

## Aktiveringsregel

En runtime får aktiveras först när den kan uppfylla samtliga följande:
1. faktisk bildgenerering,
2. A4 portrait-layout,
3. svartvit målarbild utan gråskala/skuggning,
4. referensläge med max 25 % sidhuvud,
5. åldersanpassad detaljnivå,
6. samma fallback-beteende.

Ingen canonical produktregel ändras av denna bedömning.
