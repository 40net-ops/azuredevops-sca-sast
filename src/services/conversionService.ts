import type { Unit, ConversionResult } from '@/types/units'

export class ConversionService {
  /**
   * Convert a value from one unit to another
   */
  static convert(value: number, fromUnit: Unit, toUnit: Unit): ConversionResult {
    // Check if conversion is valid (same category)
    if (fromUnit.category !== toUnit.category) {
      throw new Error(
        `Cannot convert between different categories: ${fromUnit.category} and ${toUnit.category}`
      )
    }

    let convertedValue: number
    let formula: string

    if (fromUnit.category === 'storage') {
      // Convert storage units
      const valueInBytes = value * (fromUnit.bytesMultiplier || 1)
      convertedValue = valueInBytes / (toUnit.bytesMultiplier || 1)
      formula = this.getStorageFormula(value, fromUnit, toUnit, convertedValue)
    } else {
      // Convert transfer units
      const valueInBps = value * (fromUnit.bitsPerSecondMultiplier || 1)
      convertedValue = valueInBps / (toUnit.bitsPerSecondMultiplier || 1)
      formula = this.getTransferFormula(value, fromUnit, toUnit, convertedValue)
    }

    return {
      value: convertedValue,
      fromUnit,
      toUnit,
      formula,
    }
  }

  /**
   * Format a number for display with appropriate precision
   */
  static formatNumber(value: number): string {
    // Handle very small numbers
    if (value !== 0 && Math.abs(value) < 0.0001) {
      return value.toExponential(6)
    }

    // Handle very large numbers
    if (Math.abs(value) >= 1e15) {
      return value.toExponential(6)
    }

    // Handle normal numbers
    if (Number.isInteger(value)) {
      return value.toLocaleString()
    }

    // For decimals, show up to 10 significant digits
    const formatted = value.toPrecision(10)
    const parsed = parseFloat(formatted)
    return parsed.toLocaleString(undefined, { maximumFractionDigits: 10 })
  }

  /**
   * Generate storage conversion formula
   */
  private static getStorageFormula(
    value: number,
    fromUnit: Unit,
    toUnit: Unit,
    result: number
  ): string {
    const fromMultiplier = fromUnit.bytesMultiplier || 1
    const toMultiplier = toUnit.bytesMultiplier || 1

    if (fromUnit.key === toUnit.key) {
      return `${this.formatNumber(value)} ${fromUnit.label} = ${this.formatNumber(result)} ${toUnit.label}`
    }

    const ratio = fromMultiplier / toMultiplier
    return `${this.formatNumber(value)} ${fromUnit.label} × ${this.formatNumber(ratio)} = ${this.formatNumber(result)} ${toUnit.label}`
  }

  /**
   * Generate transfer rate conversion formula
   */
  private static getTransferFormula(
    value: number,
    fromUnit: Unit,
    toUnit: Unit,
    result: number
  ): string {
    const fromMultiplier = fromUnit.bitsPerSecondMultiplier || 1
    const toMultiplier = toUnit.bitsPerSecondMultiplier || 1

    if (fromUnit.key === toUnit.key) {
      return `${this.formatNumber(value)} ${fromUnit.label} = ${this.formatNumber(result)} ${toUnit.label}`
    }

    const ratio = fromMultiplier / toMultiplier
    return `${this.formatNumber(value)} ${fromUnit.label} × ${this.formatNumber(ratio)} = ${this.formatNumber(result)} ${toUnit.label}`
  }

  /**
   * Validate if a conversion is possible
   */
  static canConvert(fromUnit: Unit | null, toUnit: Unit | null): boolean {
    if (!fromUnit || !toUnit) return false
    return fromUnit.category === toUnit.category
  }
}
