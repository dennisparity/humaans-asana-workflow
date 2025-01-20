# humaans-asana-workflow

Humaans -> Asana Bot to kickstart a couple of people processes by adding relevant personal fields into an Asana task to trigger automated workflows

## Prerequisite

**1.** Make sure you have Python 3.10+ installed on your machine

**2.** Install required dependencies

pip3 install -r requirements.txt
```

**3.** Run the script you want using the new virtual environment created by Poetry.

```
ASANA_TOKEN='...' python3 <your_script.py>
```

## Scripts

### OpenGov Proposal Tracking

- **Script:** [proposal_tracking.py](proposal_tracking.py)
- **Board:** https://app.asana.com/0/1204933329646223/board
- **Interval**: hourly
- **TLDR:** Tracks all new proposals/referendums on OpenGov and adds them to the board in Asana. Updates existing ones if necessary.

```
ASANA_TOKEN='...' python3 proposal_tracking.py
```

### OpenGov Referendum Dashboard

- **Script:** [referendum_dashboard.py](referendum_dashboard.py)
- **Board:** https://app.asana.com/0/1204999753563279/list
- **Interval**: hourly
- **TLDR:** Tracks referendums from specified tracks (11, 31, 32, etc) and tabulates them in Asana for easier observation of what's going on.

```
ASANA_TOKEN='...' python3 referendum_dashboard.py
```
