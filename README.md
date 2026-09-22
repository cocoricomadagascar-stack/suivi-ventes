# Suivi Ventes — App Android

Cette petite application affiche ton Google Sheet en plein écran, comme une vraie app.
GitHub la compile pour toi (gratuitement) : tu n'installes rien sur ton ordinateur.

## Étapes

1. **Modifie l'adresse de ton Google Sheet**
   Ouvre `app/src/main/res/values/strings.xml` et remplace la ligne `target_url`
   par le lien de ton fichier (copié depuis Chrome, onglet "Saisie" ouvert).

2. **Crée un dépôt GitHub**
   Sur github.com → "New repository" → nomme-le (ex: `suivi-ventes`) → Create.

3. **Mets tous ces fichiers dans le dépôt**
   "Add file" → "Upload files" → fais glisser tout le contenu de ce dossier
   (en gardant la structure des sous-dossiers) → "Commit changes".

4. **Lance la construction**
   Onglet "Actions" du dépôt → si demandé, active les workflows → le build
   démarre automatiquement (ou clique "Run workflow"). Attends 3–5 minutes.

5. **Télécharge l'APK**
   Une fois le run vert ✅, ouvre-le → en bas, section "Artifacts" →
   télécharge `suivi-ventes-apk` (c'est un .zip contenant `app-debug.apk`).

6. **Installe-la sur le téléphone**
   Transfère le .apk sur le téléphone (WhatsApp à soi-même, Google Drive, câble USB...).
   Ouvre-le → Android demande d'autoriser "Installer des apps inconnues" pour
   cette source → accepte → Installer.

## Remarques

- C'est une version "debug" (non signée pour le Play Store) — normal et sans
  problème pour un usage interne, sideloadé sur vos propres téléphones.
- Si tu changes le lien du Google Sheet plus tard, remets à jour `strings.xml`
  et relance simplement "Run workflow" dans l'onglet Actions pour régénérer l'APK.
- Chaque caissier doit être connecté à son compte Google dans l'app (WebView)
  pour accéder au fichier partagé, comme dans un navigateur normal.
