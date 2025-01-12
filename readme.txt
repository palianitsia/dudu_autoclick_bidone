### Requisiti per l'AutoClicker

#### Requisiti di Sistema
- **Sistema Operativo**:
  - Windows, macOS o Linux (con supporto per Python 3.7 o superiore).
- **Hardware**:
  - Processore moderno a 64-bit.
  - Almeno 2 GB di RAM.
  - Accesso a Internet per il download e l'installazione dei browser.

#### Requisiti Software
- **Python**:
  - Versione 3.7 o superiore.
- **Moduli Python richiesti**:
  - `PyQt5`
  - `pyautogui`
  - `playwright`
  - `qasync`
  - `requests`
  - Eventuali dipendenze installabili automaticamente con `pip`.

#### Browser
- **Browser supportati**:
  - Google Chrome
  - Mozilla Firefox
- **Installazione automatica**:
  - Se non già presenti, i browser saranno installati automaticamente (richiede i permessi di amministratore).

#### Configurazione opzionale
- **File di configurazione** (`config.txt`):
  - Specifica i percorsi personalizzati per i browser (Chrome o Firefox) se installati in directory non standard.

#### Installazione dei requisiti
1. Installare Python:
   - Scaricare e installare Python 3.7+ da [python.org](https://www.python.org/).
   - Assicurarsi che `pip` sia installato.

2. Installare i moduli richiesti:
   ```bash
   pip install PyQt5 pyautogui playwright qasync requests
   ```

3. Configurare Playwright:
   - Inizializzare Playwright eseguendo:
     ```bash
     playwright install
     ```

4. Verifica browser:
   - Assicurarsi che Google Chrome o Mozilla Firefox siano installati. In alternativa, consentire allo script di installarli automaticamente.

#### Esecuzione dello script
- Avviare il file principale:
  ```bash
  python nome_file.py
  ```
- Seguire le istruzioni dell'interfaccia utente per configurare il clic automatico o il monitoraggio delle aste.

#### Note aggiuntive
- **Permessi di amministratore**: Alcune funzionalità, come l'installazione dei browser, potrebbero richiedere privilegi elevati.
- **Configurazioni avanzate**:
  - Modificare il file `config.txt` per specificare percorsi personalizzati ai browser.

