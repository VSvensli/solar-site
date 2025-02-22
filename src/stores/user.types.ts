export type UserFunds = {
  accountBalance: number;
};

export type UserProject = {
  projectId: string;
  cellIds: string[];
  percentageOwned: number;
};

export type UserPerformaceDataPoint = {
  timestamp: string;
  value: number;
};

// Maybe ?
export type User = {
  id: string;
  email: string;
  funds: UserFunds;
  projects: UserProject[];
};
