export type UnitCategory = 'storage' | 'transfer'

export interface Unit {
  key: string
  label: string
  category: UnitCategory
  bytesMultiplier?: number // For storage units
  bitsPerSecondMultiplier?: number // For transfer units
  description: string
}

export interface ConversionResult {
  value: number
  fromUnit: Unit
  toUnit: Unit
  formula: string
}
