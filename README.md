# Craigslist Keyword Watcher (Python 3)

A small script that watches Craigslist search results for **new posts** and sends an alert when a post body contains any of your configured **keywords**.

This version:

* Runs on **Python 3**
* Scrapes Craigslist **HTML search results** (not RSS)
* Sends mail via **local `sendmail` / `ssmtp`** (no SMTP creds in the script)
* Avoids duplicate alerts with a **seen-state JSON file**
* Prints a clear summary so it doesn’t exit silently

---

## Features

* Search Craigslist by **region + category** (+ optional query)
* Parse multiple Craigslist result layouts (new + older)
* Fetch each post and scan `<section id="postingbody">`
* Match keywords **case-insensitively**
* Send alerts using your box’s mail setup (e.g. `ssmtp` sendmail emulation)
* Dedupe across runs (`seen_craigslist.json`)
* Pagination, throttling, loop/polling mode, dry-run mode
* Optional mail debug output

---

## Requirements

### System

* Python **3.10+** recommended 
* A configured local mailer providing `sendmail` or `ssmtp`

  * On many hosts, `sendmail` is a symlink to `/usr/sbin/ssmtp`

### Python packages

* `requests`
* `beautifulsoup4`

Install:

```bash
python3 -m pip install --user requests beautifulsoup4
```

---

## Setup

### 1) Configure destination (required)

The script reads destination info from environment variables.

Required:

* `ALERT_TO` — destination email or email-to-SMS gateway

Optional:

* `ALERT_FROM` — From header address
* `MAIL_DEBUG` — set to `1` to run mailer verbose and print output

Example:

```bash
export ALERT_TO="you@gmail.com"
export ALERT_FROM="you@gmail.com"
```

### 2) Confirm local mailer exists

Check what `sendmail` points to:

```bash
command -v sendmail
readlink -f "$(command -v sendmail)"
```

On Ubuntu with sSMTP, this often shows:

```
/usr/sbin/ssmtp
```

---

## Usage

Basic run:

```bash
python3 craigslist_watch.py --region boston --category gms --keywords "mario,ps5,nintendo"
```

Run with a Craigslist search query:

```bash
python3 craigslist_watch.py --region boston --category gms --query "garage sale" --keywords "nintendo,gameboy"
```

Scan multiple search pages (pagination):

```bash
python3 craigslist_watch.py --region boston --category gms --pages 2 --keywords "xbox,ps5"
```

Loop/poll every 5 minutes:

```bash
python3 craigslist_watch.py --region boston --category gms --keywords "mario,ps5" --loop 300
```

Dry-run (prints matches, sends nothing):

```bash
python3 craigslist_watch.py --region boston --category gms --keywords "mario,ps5" --dry-run
```

Throttle requests more gently (reduces chance of blocks):

```bash
python3 craigslist_watch.py --region boston --category gms --sleep 3.0 --keywords "mario,ps5"
```

---

## CLI Options

| Option        |                Default | Description                                              |
| ------------- | ---------------------: | -------------------------------------------------------- |
| `--region`    |               `boston` | Craigslist subdomain (e.g. `boston`, `newyork`, `sfbay`) |
| `--category`  |                  `gms` | Craigslist category path (e.g. `gms`, `sss`, etc.)       |
| `--query`     |                 (none) | Optional search query string                             |
| `--keywords`  |          built-in list | Comma-separated keywords to match                        |
| `--seen-file` | `seen_craigslist.json` | JSON file for dedupe state                               |
| `--pages`     |                    `1` | How many search pages to scan                            |
| `--page-size` |                  `120` | Offset step for pagination (`s=`)                        |
| `--sleep`     |                  `1.5` | Seconds to sleep between HTTP requests                   |
| `--loop`      |                    `0` | If >0, rerun every N seconds                             |
| `--dry-run`   |                    off | Print matches; do not send email                         |

---

## Carrier Email-to-SMS Gateways (examples)

You can send to an email-to-SMS gateway address as `ALERT_TO`. Note: reliability varies by carrier and region.

Examples:

* AT&T: `number@txt.att.net` or `number@mms.att.net`
* Verizon: `number@vtext.com`
* T-Mobile: `number@tmomail.net`

Example:

```bash
export ALERT_TO="6175551212@vtext.com"
```

---

## Output Behavior

The script always prints a summary at the end of a run. For example:

* No new posts:

  * `No new posts to scan ... nothing to send.`
* New posts but no matches:

  * `Scanned X new posts ... no keyword matches; nothing to send via email.`
* Matches found:

  * Prints `[alert] match 'keyword' -> URL` per match and a final summary.

So it won’t leave you wondering if it did anything at the end.

---

## Troubleshooting

### 1) “It runs but I get no email”

Most common: **no keyword matches**. Try a very common keyword like `sale` or run with dry-run:

```bash
python3 craigslist_watch.py --region boston --category gms --keywords "sale" --dry-run
```

### 2) Verify mail handoff works from the script

Enable verbose mail debug output:

```bash
export MAIL_DEBUG=1
python3 craigslist_watch.py --region boston --category gms --keywords "sale"
```

This prints the mailer command, return code, and verbose output from `ssmtp/sendmail` so you can confirm delivery without mystery.

### 3) Craigslist block page

If you get an error like “Craigslist returned a blocked page”, your host/IP/network is getting filtered. Things that help:

* Increase `--sleep` (e.g. 3–5 seconds)
* Scan fewer pages (`--pages 1`)
* Don’t run too frequently (`--loop 600` instead of 60)
* Ensure a realistic User-Agent (script sets one by default)

### 4) Where are mail logs on Ubuntu 24.04?

If you’re using `ssmtp` sendmail emulation, there’s typically **no queue** and log entries vary. The fastest truth is `MAIL_DEBUG=1`.

If you have a full MTA (Postfix/Exim), logs are usually:

* `/var/log/mail.log`
* `journalctl -u postfix`

---

## Notes on “seen” state

The file `seen_craigslist.json` stores listing IDs already processed. This prevents duplicates across runs.

If you want to “start fresh” (re-alert on old listings), delete it:

```bash
rm -f seen_craigslist.json
```

---

## Legal / Courtesy

Be a decent internet citizen: don’t hammer Craigslist. Use throttling (`--sleep`) and reasonable polling intervals (`--loop`). Thanks. 
