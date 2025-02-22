export type UserStatistics = {
  accountBalance: number;
  cellsOwned: number;
  projectsOwned: number;
  totalInvested: number;
  totalEarnings: number;
  totalEnergyGenerated: number;
  maximumPowerGeneration: number;
};

export type UserProject = {
  projectId: string;
  cellIds: string[];
  percentageOwned: number;
  timeOfPurchase: Date;
};

export type UserPerformaceDataPoint = {
  timestamp: string;
  value: number;
};

// Maybe ?
export type User = {
  id: string;
  email: string;
  statistics: UserStatistics;
  projects: UserProject[];
};
