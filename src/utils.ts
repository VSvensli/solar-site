/**
 * This function takes a number which represents a power. It converts this to a string value with unit suffix.
 * @param value
 * @returns string
 */
export function formatPower(value: number): string {
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
export function formatEnergy(value: number): string {
  if (value < 1000) {
    return `${value} Wh`;
  } else if (value < 1000000) {
    return `${(value / 1000).toFixed(2)} kWh`;
  } else {
    return `${(value / 1000000).toFixed(2)} MWh`;
  }
}

/**
 * This function takes a number which represents a money. It converts this to a string value with unit suffix.
 * @param value
 * @returns string
 */
export function formatDollar(value: number): string {
  const [intPart, decPart] = value.toFixed(2).split(".");
  let formatted = "";
  const len = intPart.length;

  for (let i = 0; i < len; i++) {
    formatted += intPart[i];
    if ((len - i - 1) % 3 === 0 && i !== len - 1) {
      formatted += " ";
    }
  }

  return `$${formatted}.${decPart}`;
}
