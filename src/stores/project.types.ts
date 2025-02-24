export type Project = {
  projectId: string;
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
  cellId: string;
  ownerId: string;
  price: number;
  cellIndex: number;
  color: string;
};

export type Panel = {
  projectId: string;
  panelId: string;
  description: string;
  cellRows: number;
  cellColumns: number;
  cells: Cell[];
};
