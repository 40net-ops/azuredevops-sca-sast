import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Unit, ConversionResult } from '@/types/units'
import { ConversionService } from '@/services/conversionService'
import { STORAGE_UNITS, TRANSFER_UNITS } from '@/utils/constants'

export const useConversionStore = defineStore('conversion', () => {
  // State
  const inputValue = ref<string>('')
  const fromUnit = ref<Unit | null>(STORAGE_UNITS[1] || null) // Default to Byte
  const toUnit = ref<Unit | null>(STORAGE_UNITS[6] || null) // Default to GB
  const result = ref<ConversionResult | null>(null)
  const error = ref<string | null>(null)

  // Getters
  const availableFromUnits = computed(() => {
    return [...STORAGE_UNITS, ...TRANSFER_UNITS]
  })

  const availableToUnits = computed(() => {
    if (!fromUnit.value) return []
    return fromUnit.value.category === 'storage' ? STORAGE_UNITS : TRANSFER_UNITS
  })

  const formattedResult = computed(() => {
    if (!result.value) return null
    return ConversionService.formatNumber(result.value.value)
  })

  const canPerformConversion = computed(() => {
    return (
      inputValue.value !== '' &&
      !isNaN(parseFloat(inputValue.value)) &&
      fromUnit.value !== null &&
      toUnit.value !== null &&
      ConversionService.canConvert(fromUnit.value, toUnit.value)
    )
  })

  // Actions
  function performConversion() {
    error.value = null
    result.value = null

    if (!canPerformConversion.value) {
      error.value = 'Please enter a valid number and select units'
      return
    }

    try {
      const value = parseFloat(inputValue.value)
      result.value = ConversionService.convert(value, fromUnit.value!, toUnit.value!)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Conversion failed'
    }
  }

  function setInputValue(value: string) {
    inputValue.value = value
    if (canPerformConversion.value) {
      performConversion()
    }
  }

  function setFromUnit(unit: Unit) {
    fromUnit.value = unit

    // If switching categories, reset toUnit to first unit of new category
    if (toUnit.value && toUnit.value.category !== unit.category) {
      toUnit.value = (unit.category === 'storage' ? STORAGE_UNITS[0] : TRANSFER_UNITS[0]) || null
    }

    if (canPerformConversion.value) {
      performConversion()
    }
  }

  function setToUnit(unit: Unit) {
    toUnit.value = unit
    if (canPerformConversion.value) {
      performConversion()
    }
  }

  function swapUnits() {
    if (!fromUnit.value || !toUnit.value) return

    const temp = fromUnit.value
    fromUnit.value = toUnit.value
    toUnit.value = temp

    // Update input with result value if available
    if (result.value) {
      inputValue.value = result.value.value.toString()
    }

    performConversion()
  }

  function reset() {
    inputValue.value = ''
    fromUnit.value = STORAGE_UNITS[1] || null // Byte
    toUnit.value = STORAGE_UNITS[6] || null // GB
    result.value = null
    error.value = null
  }

  return {
    // State
    inputValue,
    fromUnit,
    toUnit,
    result,
    error,

    // Getters
    availableFromUnits,
    availableToUnits,
    formattedResult,
    canPerformConversion,

    // Actions
    performConversion,
    setInputValue,
    setFromUnit,
    setToUnit,
    swapUnits,
    reset,
  }
})
