# ESPHome

## Pre-requisites

1. Docker. You may follow [this guide](https://www.docker.com/get-started/) to obtain it.
2. [AWS set up](../aws).

## Set Up

1. Connect your ESP8266 with a USB cable to your computer.

2. Run the following Docker container.

```bash
docker run -p 6052:6052 ghcr.io/esphome/esphome
```

3. Open `http://localhost:6052/` on your browser.

4. Click `+ NEW DEVICE`.

5. Click `CONTINUE`.

6. Under `Name`, enter `GeniusHome`. Enter also your `Network name` and `Password`. Click `NEXT`.

7. Click `SKIP THIS STEP` if prompted on installation.

8. Select `ESP8266` from the dropdown.

9. Click `SKIP` if prompted on installation.

10. Retrieve the function URL of your `HandleMCU` lambda function.

```bash
aws lambda get-function-url-config --function-name HandleMCU --query FunctionUrl --output text
```

11. Navigate to `SECRETS` and add (not replace) `HandleMCU_FUNCTION_URL: <your retrieved HandleMCU functional url>`

12. Navigate to `GeniusHome` and click `EDIT`.

13. Add (not replace) content in `geniushome_additional.yaml` to the file.

14. Click `SAVE`.

15. Click `INSTALL`.

16. Select `Plug into this computer`.

17. If you are prompted with `...://localhost:6052 wants to connect to a serial port`, select `USB2.0-Ser! (cu.usbserial-10)` and click `Connect`.
