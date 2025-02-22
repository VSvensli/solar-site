/**
 * This function takes a number which represents a power. It converts this to a string value with unit suffix.
 * @param value
 * @returns string
 */
export function parsePowerValueToString(value: number): string {
  if (value < 1000) {
    return `${value} W`;
  } else if (value < 1000000) {
    return `${(value / 1000).toFixed(2)} kW`;
  } else {
    return `${(value / 1000000).toFixed(2)} MW`;
  }
}

/**
 * This function takes a number which represents a energy. It converts this to a string value with unit suffix.
 * @param value
 * @returns string
 */
export function parseEnergyValueToString(value: number): string {
  if (value < 1000) {
    return `${value} Wh`;
  } else if (value < 1000000) {
    return `${(value / 1000).toFixed(2)} kWh`;
  } else {
    return `${(value / 1000000).toFixed(2)} MWh`;
  }
}
