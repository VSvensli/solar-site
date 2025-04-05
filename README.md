# Solar site

This is a MVP exploring the idea of fractional ownership and/or crowdfunded of solar parks. This could allow contributers to invest in solar projects to offset their carbon footprint.In addition, users can choose the color of the solar cells they purchase, allowing them to virtually "paint" the PV arrays.

# Test the app using Docker

```bash
docker pull vegardsa/solar-site:latest
docker run -d --name solar-site-host -p 80:80 vegardsa/solar-site

```

The app should then be available at http://127.0.0.1:80

# How to run dev environment

1. Setup and source python `venv`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start fastAPI backen

```bash
cd backend
fastapi dev
```

3. Start vite (Note: running with `--host` )

```bash
pnpn i
pnpn dev
```

## Todo:

- [ ] Add pagination capabilities to DBInterface
- [ ] Add faker
- [ ] Handle expired tokens
- [ ] Add proper password hashing
- [ ] Refactore \*.store.ts with unity types
- [ ] Remove primeVue as a dependecy
- [x] Add user creation
- [x] Add sqlite instead of using dicts to mock the database
- [ ] Finish checkout page and add post request for cell purchase
- [ ] Add information about power prices from Entose
- [ ] Add solar irradiateon from openweatherapi (https://openweathermap.org/api/solar-radiation)
- [ ] Replace panel selector with canvas, Pixi.js, or eqvivalent in order create a more user friendly interface for selecting cells.
- [ ] Add email validation
- [x] Add 404 page and route in routes

- [x] Dockerise
- [x] Add testing
- [ ] Add more testing
