# Anti-Infringement Certificate [ID 2561] Generator

For Fixing ZTE modem 10 minute reboot 
A Python script that generates RSA-encrypted Certificate ID 2561 for hardware validation using MAC addresses and board types.

## Requirements

```bash
pip install cryptography
```

## Usage
Run the script interactively:

```bash
python zte_certificate_generator.py
```

The script will prompt you for:
- **MAC Address 1**: MAC Address Number 1 (setmac show2 -> ID 256) (e.g., `48:96:D9:A2:47:01`)
- **MAC Address 2**: MAC Address Number 2 (setmac show2 -> ID 257) (e.g., `48:96:D9:A2:47:02`) 
- **Board Type**: Hardware board identifier (e.g., `F6600P`)

You can then input in ZTE Telnet (Example)
```bash
setmac 1 2561 U2vuqy4iIHRMZSywMc/7VrBanhx93YStMMsqDA0+ngGDmM7Rsvqkay22EWFT7qXsplEtE5MyZm6ZxXX55ss/rL86LPWUd/tTiM584+Sy5N0vyl1T8hkohT7qNPln3+PklAzpF0PSqeZcE40t45fQwSlJojnNmNewndhBJyWgzp8=
upgradetest devicecheck
```
If upgradetest results in SUCCESS you're good to go.
