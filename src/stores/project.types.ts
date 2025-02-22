export type Project = {
  id: string;
  name: string;
  locationCity: string;
  locationCountry: string;
  locationBiddingZone: string;
  installedCapacity: string;
  description: string;
  numberOfCells: number;
  unitPrice: number;
  isCompleted: boolean;
  completedDate: Date;
};

export type EnergyDataPoint = {
  timestamp: Date;
  production: number;
};

export type PowerDataPoint = {
  timestamp: Date;
  production: number;
  isPredicted: boolean;
};

export type Cell = {
  id: string;
  ownerId: string;
  price: number;
  cellRow: number;
  cellColumns: number;
  color: string;
};

export type Panel = {
  id: string;
  description: string;
  cells: Cell[];
};
