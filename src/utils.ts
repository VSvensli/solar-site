/**
 * This function takes a number which represents a power. It converts this to a string value with unit suffix.
 * @param value
 * @returns string
 */
function parsePowerValueToString(value: number): string {
  if (value < 1000) {
    return `${value} W`;
  } else if (value < 1000000) {
    return `${(value / 1000).toFixed(2)} kW`;
  } else {
    return `${(value / 1000000).toFixed(2)} MW`;
  }
}
