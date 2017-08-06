# OpenSignals Barebone

The ServerBIT is a barbone example application based on the Twisted event-driven networking engine, and designed to demonstrate the OpenSignals client-server architecture. You can use and modify the source code under the terms of the GPL licence.

This architecture is based on an asynchronous message passing protocol, in which the server and the client communicate using JSON-formatted strings. Although this code is primarily used for BITalino, it is completely general purpose.

ServerBIT receives Python instructions as string-based requests from a client, evaluates them, and replies with the same instruction having the evaluation results as input arguments.

ClientBIT is an example HTML/JS that connects to ServerBIT and opens a connection to a specified BITalino device to acquire data from A3 (ACC data as of early-2014 units) and draw it on the browser in realtime.

In our example, ClientBIT is also prepared to evaluate the strings received from the server as JS instructions.

INCOMPLETE

## Prerequisites

- Python 2.7 or above must be installed;
- BITalino API and dependencies installed;
- Twisted matrix module installed.

## Testing ServerBIT

TO_DO

## References

H. Silva, A. Lourenço, A. Fred, R. Martins. BIT: Biosignal Igniter Toolkit. Computer Methods and Programs in Biomedicine, Volume 115, 2014, Pages 20-32.

M. Lucas da Silva, D. Gonçalves, T. Guerreiro, H. Silva. A Web-Based Application to Address Individual Interests of Children with Autism Spectrum Disorders. Procedia Computer Science, Volume 14, 2012, Pages 20-27.

## Screenshots

TO_DO

