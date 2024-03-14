# OSM Ad Watcher

This is a simple script that uses Selenium to watch ads for a user in Online Soccer Manager (OSM).

Currently Ad Detection works by waiting 7 seconds after clicking the ad button for it to play and show the timer  and by finally by checking said timer

If you have PiHole or any other alternative to it consider running this script on a host machine with a different DNS i.e: 8.8.8.8 as it stands your PiHole may block the ads from loading which causes issues in the script

If you like what you see consider buying me a coffee :) https://ko-fi.com/ruicardona

## Prerequisites

- Python 3
- Firefox browser
- Selenium
- Colorama
- Have a decently high level account or be in as least two teams

## Installation

1. Clone or download the repository.
2. Install Python 3 if you haven't already.
3. Install Selenium, Colorama
4. Change the Details in details.txt to the correct ones, field order must be as is
5. Run main.py
6. Alternatively you can download the exe and follow the instructions on the releases page
