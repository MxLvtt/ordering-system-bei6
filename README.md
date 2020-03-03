# Ordering System BEI5

Group project for the fifth semester of the BEI course of studies.

# Specifications

## Group Members
* Amine Sebti
* Mohammed Jalal Meskine
* Marcel Livotto

## Topic
Development of an ordering system capable of taking in and processing food orders as well as displaying a daily summary. Purpose of this system is to safe paper and to provide a faster communication between the restaurant's kitchen and cash desk and vice versa.

## Features
1. Easy handling due to a touch screen and a clear UI.
1. Secure communication between the two stations by using encrypted messages.
1. Stable communication between the stations to prevent loss and duplication of orders (Research for appropriate ip protocols).
1. When taking in a new order there has to happen some exchange of messages between the stations in order to prevent people from injecting orders from outside.
1. At least in the kitchen station the chef has to be able to recall a history of all orders, if one accidentally deletes an order and forgets about the details while preparing the meal.
1. The whole assortment has to be stored on an external storage device or internally as e.g. a *.csv-file and can be extended very easily. This list should only be located on one of the stations (preferably on the main station - the cash desk) and the systems are synced during the boot up and whenever the file is changed.
1. In the kitchen one can mark any order as "done" or alternatively reject it. Both will also be displayed on the cash desk station.
1. The cash desk station can take in and forward new orders, as well as revoke them, even if the order is already in the queue or in progress. The latter will also be displayed in the kitchen station immediately and has to be acknowledged there to complete the revocation - this shows the cashier whether the order is already being processed or not.

## Nice to have
1. USB receipt printing device for the cash desk station
1. Possibility to export all important information onto any external storage device or to send it via email etc.

# Requirements
* 2x Raspberry Pi (+1 for development)
* 1x Touchdisplay (Cash desk)
* 1x Monitor (Kitchen)
* 1x Laser-Touch-Module for monitor
* 2x HDMI cable
* 3x Ethernet cable (Pi1 -> Sw, Pi2 -> Sw, Sw -> Network)
* 1x Network switch (4 ports)
