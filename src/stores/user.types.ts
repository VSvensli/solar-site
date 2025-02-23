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
  timestamp: Date;
  value: number;
};

export type UserInfo = {
  id: string;
  name: string;
  email: string;
};

export type UserData = {
  userInfo: UserInfo;
  statistics: UserStatistics;
  performance: UserPerformaceDataPoint[];
  projects: UserProject[];
};
