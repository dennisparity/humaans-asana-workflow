# humaans-asana-workflow

A set of periodic jobs between Humaans -> Asana to kickstart a couple of people processes by adding relevant personal details into an Asana task to trigger automated workflows.

## Prerequisite

**1.** Make sure you have Python 3.10+ installed on your machine

**2.** Install required dependencies

```
pip3 install -r requirements.txt
```

**3.** Run the script you want using the new virtual environment created by Poetry.

```
ASANA_TOKEN='...' python3 <your_script.py>
```

## Scripts

### Humaans New Joiner Tracking

- **Script:** TBC
- **Example Board:** https://app.asana.com/0/1208107121023942/1208108833959154
- **Interval**: daily
- **TLDR:** Tracks all new joiners in Humaans and adds them to the process board in Asana. Updates existing ones if necessary.

```
WIP: ASANA_TOKEN='...' python3 newjoiner_tracking.py
```
