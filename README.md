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
- **MAC Address 1**: (setmac show2 -> ID 256) (e.g., `48:96:D9:A2:47:01`) aka PON-MAC
- **MAC Address 2**: (setmac show2 -> ID 257) (e.g., `48:96:D9:A2:47:02`) aka MTA-MAC
- **Board Type**: Hardware board identifier (e.g., `F6600P`)

You can then input in ZTE Telnet (Example)
```bash
setmac 1 2561 eTjZWYYpqLkTAeX6ME7zSrlwZTYJp9ddse1YTB65IhGGbTOygyowi3A7831ooaeJS59ygmMPCCV40GFAYINiQiDzXymJXUnVD79vE/pHeBhm8zhs6APnEoAzYoR9NlpZKTEnH88vVGlm/mVbQ6ugHgq8gp6pELtJ9oWZGo26U5s=
upgradetest devicecheck
reboot
```
If upgradetest results in SUCCESS you're good to go.
