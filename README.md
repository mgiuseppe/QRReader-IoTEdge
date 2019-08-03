# Overview

La seguente soluzione IoT Edge si occupa di leggere QR e BAR CODE tramite una picamera e quando ne rivela uno:

* Invia su iot hub il testo del QR / BAR CODE rilevato
* Accende un led

## Quickstart per lo sviluppo

Sul portale azure:

* Creare un IoT Hub
  * Aggiungere un IoT Edge Device
* Creare un Azure Container Registry (abilitare accesso admin)

Sulla raspberry:

* Collegare la picamera tramite connettore CSI e un led sul GPIO 18 (ricorda la resistenza da 330!)
* Configurare il file /etc/iotedge/config.yaml inserendo la connection string dell'iot edge device creato in precedenza

Sulla solution edge (usando vs code):

* Creare un file .env nella root folder e aggiungere le seguenti variabili:
  * CONTAINER_REGISTRY_ADDRESS=XXX.azurecr.io
  * CONTAINER_REGISTRY_USERNAME_qrregistry=XXX
  * CONTAINER_REGISTRY_PASSWORD_qrregistry=XXX
* Utilizzare l'estensione Azure IoT Tools per buildare e pushare i moduli edge e per settare il deploy sul device iot edge
