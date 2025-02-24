# Solar site

This is a MVP exploring the idea of fractional ownership and/or crowdfunded of solar parks. This could allow contributers to invest in solar projects to offset their carbon footprint.In addition, users can choose the color of the solar cells they purchase, allowing them to virtually "paint" the PV arrays.

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

- [ ] Add user creation
- [ ] Add sqlite instead of using dicts to mock the database
- [ ] Finish chechout page and add post request for cell purchase
- [ ] Add information about power prices from Entose
- [ ] Add solar irradiateon from metoeblue
- [ ] Replace panel selector with canvas, Pixi.js, or eqvivalent in order create a more user friendly interface for selecting cells.

- [ ] Dockerise
- [ ] Add testing
