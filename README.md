
# Spedion Truck Import

This project provides an automated way to **transfer newly added trucks** from the **WinSped** logistics system to the **Spedion** telematics platform.

## Purpose

To ensure that vehicle information entered into WinSped is automatically and correctly registered in Spedion — reducing manual effort and synchronization errors.

This script is designed for use by logistics and IT personnel who manage fleet registration across both platforms.

## Features

- Connects to WinSped MS SQL database
- Retrieves newly added trucks (on current date)
- Sends truck information to Spedion SOAP API
- Tracks processed trucks to avoid duplicates

## Requirements

- Python 3.9+
- Access to WinSped MS SQL database
- Valid Spedion API credentials

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the script with Python:

```bash
python main.py
```

You can configure paths and credentials directly in the script (`main.py`) or externalize them later.

## Notes

- Vehicles already sent to Spedion are tracked using a `LIST_PATCH.txt` file to prevent duplicates.
- Ensure firewall and access permissions allow database and API communication.

## License

This project is intended for internal automation. Licensing TBD.

---

**Maintained by:** Chr. Carstensen Logistics

---

[![LinkedIn](https://example.com/linkedin-icon.png)](https://www.linkedin.com/in/alex-weiss-a6483417b)

[Spedion_Driver_Uploader](https://github.com/weissalexey/Spedion_Driver_Uploader/edit/main/README.md)
