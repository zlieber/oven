# Composite curing oven controller UI for Raspberry PI

Composite curing ovens are used to cure out-of-autoclave (OOA) prepregs, post-cure high-temperature epoxies and others.

Usually a curing schedule involves raising the temperature gradually at a certain rate, then maintaining (dwelling on) the target temperature for a few hrs before moving on to next stage.

This code uses Raspberry PI or similar together with a touch screen and a relay control to provide an easy UI for your oven.

## Hardware

Raspberry PI or similar (I tested with Rock PI)
Touch screen (tested with 7in HDMI)
Relay. Solid-state relay (SSR) is recommended

## Installation

Relay is currently controlled via GPIO pin (71 on Rock PI)

Depending on heating element and power requirements, a second stage relay may be needed.

LightDM or similar display manager should be installed on the device.

Set up auto-login for user and auto-start for the application, and it should all be ready to go.
