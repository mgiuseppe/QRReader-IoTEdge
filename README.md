# Overview

Questa soluzione IoT Edge si occupa di leggere QR e BAR CODE tramite una picamera e quando ne rivela uno:

* Inviare su iot hub il testo del QR / BAR CODE rilevato
* Accendere un led

## Quickstart per lo sviluppo

Sul portale azure:

* Creare un IoT Hub
  * Aggiungere un IoT Edge Device
* Creare un Azure Container Registry (abilitare accesso admin)

Sulla raspberry:

* Installare l'edge runtime sulla raspberry
* Collegare la picamera tramite connettore CSI e un led sul GPIO 18 (ricorda la resistenza da 330!)
* Configurare il file /etc/iotedge/config.yaml inserendo la connection string dell'iot edge device creato in precedenza

Sulla solution edge (usando vs code):

* Creare un file .env nella root folder e aggiungere le seguenti variabili:
  * CONTAINER_REGISTRY_ADDRESS=XXX.azurecr.io
  * CONTAINER_REGISTRY_USERNAME_qrregistry=XXX
  * CONTAINER_REGISTRY_PASSWORD_qrregistry=XXX
* Utilizzare l'estensione Azure IoT Tools per buildare le immagini docker dei moduli edge e pusharle sul container registry e per settare il target deploy per il device edge
