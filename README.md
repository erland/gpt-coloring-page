# Målarbilds-generator GPT

Detta paket innehåller material för att skapa en egen GPT som hjälper användaren att skapa utskrivbara målarbilder utifrån:

- motivbeskrivning
- ungefärlig ålder på barnet/målaren
- önskat format: bara målarbild eller liten färglagd referens + stor målarbild

GPT:n är tänkt för privat kreativ användning och ska vara särskilt bra på barnvänliga, tydliga och utskrivbara A4-målarbilder.

## Innehåll

- `gpt-instructions.md` – huvudtext att klistra in i GPT:ns instruktioner.
- `conversation-starters.md` – förslag på conversation starters.
- `knowledge/age-complexity-guide.md` – stöd för åldersanpassning.
- `knowledge/layout-and-print-guide.md` – regler för A4-layout och referensbild.
- `knowledge/fallback-prompt-guide.md` – hur GPT:n ska föreslå alternativa prompts om en bild inte kan skapas.
- `examples/example-prompts.md` – exempel på bra färdiga bildprompts.

## Rekommenderad GPT-konfiguration

### Name
Målarbilds-generatorn

### Description
Skapar utskrivbara A4-målarbilder för barn och vuxna utifrån motiv, ålder och önskad detaljnivå. Kan även skapa en liten färglagd referens högst upp och en stor svartvit målarbild nedanför.

### Instructions
Klistra in innehållet från `gpt-instructions.md`.

### Knowledge
Ladda gärna upp filerna i `knowledge/` som kunskapsfiler.

### Capabilities
Aktivera bildgenerering.
Web browsing behövs normalt inte.


## Distributionspaket

Repositoryt kan bygga två distributionsformat från samma aktuella GPT-konfiguration:

- `coloring-page-custom-gpt-vX.Y.Z.zip` för installation/uppdatering av Custom GPT.
- `coloring-page-chat-vX.Y.Z.zip` för att bifogas direkt i en vanlig ChatGPT-konversation.

Kör lokalt:

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

Vanliga byggen använder `VERSION`. Vid en publicerad GitHub Release används release-taggen som versionskälla. En release `v1.1.0` producerar automatiskt båda `...v1.1.0.zip` och bifogar dem till releasen.

Custom GPT-paketets huvudinstruktion, conversation starters och tre Knowledge-filer kopieras utan innehållsförändring från de kanoniska källorna.
