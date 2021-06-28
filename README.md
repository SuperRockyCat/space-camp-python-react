# Space Camp Demo App: React + Python

## App Overview
A small Python + React application intended to be used for training users on the core functionality of the LaunchDarkly SDK. The front-end (React) component will log any feature flag updates as they are made either in the `./api/api.py` Python file, or in the LaunchDarkly Dashboard. 

Users can set the value of the `ld_sdk_key` variable in  `./api/api.py` to their environment, and implement an `ld_client.variation` call of their choice on line 37. Once implemented the front end will log updates to the flag as they occur. Users can implement rules based targeting and percentage rollouts live and see how that impacts the variation assignment.


## How to Run
This project is dockerized and should be easy to run without installing any dependencies manually. [Docker desktop](https://www.docker.com/products/docker-desktop) must be installed prior to following the steps below:

- Clone this repo: `git clone https://github.com/SuperRockyCat/space-camp-python-react.git`
- `cd space-camp-python-react`
- `docker-compose up`